import sys
from rdkit import Chem
from rdkit.Chem import BRICS, Descriptors, AllChem
from rdkit.Chem.Scaffolds import MurckoScaffold

def sanitize_mol(mol):
    """Attempt to sanitize molecule with various approaches"""
    if mol is None:
        return None
    
    try:
        # Try normal sanitization first
        Chem.SanitizeMol(mol)
        return mol
    except:
        try:
            # If normal sanitization fails, try step-by-step
            Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_ALL^Chem.SANITIZE_KEKULIZE)
            Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_KEKULIZE)
            return mol
        except:
            try:
                # If kekulization fails, try removing aromatic flags
                for atom in mol.GetAtoms():
                    atom.SetIsAromatic(False)
                for bond in mol.GetBonds():
                    bond.SetIsAromatic(False)
                Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_ALL^Chem.SANITIZE_KEKULIZE)
                Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_KEKULIZE)
                return mol
            except:
                return None

def clean_smiles(smiles):
    """Remove attachment points and clean SMILES with better sanitization"""
    try:
        # Convert SMILES to mol
        mol = Chem.MolFromSmiles(smiles, sanitize=False)
        if mol is None:
            return None
        
        # Try to sanitize the molecule
        mol = sanitize_mol(mol)
        if mol is None:
            return None
        
        # Replace explicit hydrogens with implicit ones
        mol = Chem.RemoveHs(mol)
        
        # Generate canonical SMILES
        return Chem.MolToSmiles(mol, canonical=True)
    except:
        return None

def fragment_via_brics(mol, min_size=3):
    """Fragment using BRICS with better error handling"""
    fragments = []
    try:
        for frag in BRICS.BRICSDecompose(mol, minFragmentSize=min_size):
            clean_frag = clean_smiles(frag)
            if clean_frag:
                fragments.append(clean_frag)
    except:
        pass
    return fragments

def fragment_bonds(mol, bond_types=None):
    """Fragment by breaking specified bond types with improved chemical handling"""
    if bond_types is None:
        bond_types = [Chem.BondType.SINGLE]  # Removed double bond breaking to reduce invalid fragments
    
    fragments = []
    bonds = []
    
    # Only break bonds that aren't in aromatic rings
    for bond in mol.GetBonds():
        if (bond.GetBondType() in bond_types and 
            not bond.IsInRing() and 
            not (bond.GetBeginAtom().GetIsAromatic() and bond.GetEndAtom().GetIsAromatic())):
            bonds.append(bond.GetIdx())
    
    # Fragment on individual bonds
    for bond_idx in bonds:
        try:
            broken = Chem.FragmentOnBonds(mol, [bond_idx], addDummies=False)
            frags = Chem.GetMolFrags(broken, asMols=True, sanitizeFrags=False)
            for frag in frags:
                sanitized_frag = sanitize_mol(frag)
                if sanitized_frag:
                    clean_frag = clean_smiles(Chem.MolToSmiles(sanitized_frag))
                    if clean_frag:
                        fragments.append(clean_frag)
        except:
            continue
    
    return fragments

def fragment_rings(mol):
    """Fragment ring systems with better chemical handling"""
    fragments = []
    ring_info = mol.GetRingInfo()
    
    # Only process non-aromatic rings
    for ring in ring_info.AtomRings():
        # Check if ring is aromatic
        is_aromatic = False
        for idx in ring:
            if mol.GetAtomWithIdx(idx).GetIsAromatic():
                is_aromatic = True
                break
        
        if not is_aromatic:
            try:
                # Create a new molecule with just the ring atoms
                ring_mol = Chem.PathToSubmol(mol, ring)
                if ring_mol is not None:
                    sanitized_ring = sanitize_mol(ring_mol)
                    if sanitized_ring:
                        clean_frag = clean_smiles(Chem.MolToSmiles(sanitized_ring))
                        if clean_frag:
                            fragments.append(clean_frag)
            except:
                continue
    
    return fragments

def fragment_scaffolds(mol):
    """Fragment using Murcko scaffolds with better sanitization"""
    fragments = []
    
    try:
        # Get Murcko scaffold
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
        if scaffold is not None:
            sanitized_scaffold = sanitize_mol(scaffold)
            if sanitized_scaffold:
                clean_frag = clean_smiles(Chem.MolToSmiles(sanitized_scaffold))
                if clean_frag:
                    fragments.append(clean_frag)
    except:
        pass
    
    return fragments

def is_valid_fragment(mol):
    """Enhanced validation of fragments"""
    if mol is None:
        return False
    
    # Basic criteria
    if mol.GetNumAtoms() < 3:  # Increased minimum size
        return False
    
    if all(atom.GetSymbol() == 'C' for atom in mol.GetAtoms()):
        return False
    
    # Check for invalid valences
    try:
        Chem.SanitizeMol(mol, sanitizeOps=Chem.SANITIZE_PROPERTIES)
    except:
        return False
    
    # Additional chemical checks
    for atom in mol.GetAtoms():
        # Check for unusual valences
        if atom.GetImplicitValence() < 0:
            return False
        # Check for charged atoms (optional, remove if you want charged fragments)
        if atom.GetFormalCharge() != 0:
            return False
    
    return True

def generate_fragments(input_file, output_file, min_mw=100, max_mw=150):
    seen = set()
    error_count = 0
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line_num, line in enumerate(f_in, 1):
            smiles = line.strip().split()[0]
            mol = Chem.MolFromSmiles(smiles, sanitize=False)
            if mol is None:
                continue
            
            # Sanitize input molecule
            mol = sanitize_mol(mol)
            if mol is None:
                error_count += 1
                continue
            
            # Generate fragments
            fragments = []
            fragments.extend(fragment_via_brics(mol))
            fragments.extend(fragment_bonds(mol))
            fragments.extend(fragment_rings(mol))
            fragments.extend(fragment_scaffolds(mol))
            
            # Filter and write unique fragments
            for frag_smi in fragments:
                try:
                    frag_mol = Chem.MolFromSmiles(frag_smi, sanitize=False)
                    if frag_mol is None:
                        continue
                    
                    frag_mol = sanitize_mol(frag_mol)
                    if not frag_mol or not is_valid_fragment(frag_mol):
                        continue
                    
                    mw = Descriptors.MolWt(frag_mol)
                    if min_mw <= mw <= max_mw:
                        canonical_smi = Chem.MolToSmiles(frag_mol, canonical=True)
                        if canonical_smi not in seen:
                            seen.add(canonical_smi)
                            f_out.write(f"{canonical_smi}\n")
                except:
                    continue
    
    return len(seen), error_count

if __name__ == "__main__":
    input_file = "inhibitors_for_fragmentations.smi"    #Update this file if you want to fragment other libraries
    output_file = "fragment_from_inhibitors.smi"
    
    n_fragments, n_errors = generate_fragments(
        input_file=input_file,
        output_file=output_file,
        min_mw=100,
        max_mw=150
    )
    
    print(f"Done! Generated {n_fragments} fragments with {n_errors} errors.")
    print(f"Output saved to: {output_file}")
