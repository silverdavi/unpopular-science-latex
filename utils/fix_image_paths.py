#!/usr/bin/env python3

import os
import re
import glob

def fix_image_paths():
    """Fix all image paths in LaTeX files to use indexed folder names"""
    
    # Define the mapping from old folder names to new indexed names
    folder_mapping = {
        'BanachTarskiParadox': '01_BanachTarskiParadox',
        'TopologicalInsulators': '02_TopologicalInsulators', 
        'GoldRelativity': '03_GoldRelativity',
        'EMFieldsEnergyFlow': '04_EMFieldsEnergyFlow',
        'CircleWheel': '05_CircleWheel',
        'GravityTimeDilation': '06_GravityTimeDilation',
        'BilliardsConicsPorism': '07_BilliardsConicsPorism',
        'BoundedPrimeGaps': '08_BoundedPrimeGaps',
        'ArrowTheoremTopology': '09_ArrowTheoremTopology',
        'SolarFusionQuantumTunneling': '10_SolarFusionQuantumTunneling',
        'AcceleratingUniverse': '11_AcceleratingUniverse',
        'GSMEncryptionOrder': '12_GSMEncryptionOrder',
        'PoissonsSpot': '13_PoissonsSpot',
        'CompactTwinParadox': '14_CompactTwinParadox',
        'EnvelopeParadox': '15_EnvelopeParadox',
        'ShoelaceKnotMechanics': '16_ShoelaceKnotMechanics',
        'TorricellisTrumpet': '17_TorricellisTrumpet',
        'SpeculativeExecutionAttacks': '18_SpeculativeExecutionAttacks',
        'CosmicRayMuons': '19_CosmicRayMuons',
        'ChineseRoomArgument': '20_ChineseRoomArgument',
        'ExponentialMapsLieTheory': '21_ExponentialMapsLieTheory',
        'MinecraftCreeper': '22_MinecraftCreeper',
        'BlackHoleTimeDilationRedshift': '23_BlackHoleTimeDilationRedshift',
        'FourDSpacetime': '24_FourDSpacetime',
        'FireflyBioluminescence': '25_FireflyBioluminescence',
        'ZKProofs': '26_ZKProofs',
        'PlanetarySkyColors': '27_PlanetarySkyColors',
        'NegativeTemp': '28_NegativeTemp',
        'HatMonotile': '29_HatMonotile',
        'SimpsonsParadox': '30_SimpsonsParadox',
        'osmosis_Debye': '31_osmosis_Debye',
        'AtomicClocks': '32_AtomicClocks',
        'IncubationInequality': '33_IncubationInequality',
        'BoltzmannBrain': '34_BoltzmannBrain',
        'TreesFromAir': '35_TreesFromAir',
        'qft_vs_gr': '36_qft_vs_gr',
        'DarkMatterEvidence': '37_DarkMatterEvidence',
        'ChristmasTruce1914': '38_ChristmasTruce1914',
        'SuperpermutationsBreakthrough': '39_SuperpermutationsBreakthrough',
        'BoomerangFlight': '40_BoomerangFlight',
        'HoughTransfrom': '41_HoughTransfrom',
        'IceSlipperiness': '42_IceSlipperiness',
        'NearFlatUniverse': '43_NearFlatUniverse',
        'IronMask': '44_IronMask',
        'MaxwellDemon': '45_MaxwellDemon',
        'WoodwardHoffmannRules': '46_WoodwardHoffmannRules',
        'ObserverDependentVacuum': '47_ObserverDependentVacuum',
        'three_body': '48_three_body',
        'IVFmtDNA': '49_IVFmtDNA',
        'LangtonsAnt': '50_LangtonsAnt',
        'QuantumSubspaceAngles': '52_QuantumSubspaceAngles',
        'BodySwappingPuzzle': '53_BodySwappingPuzzle'
    }
    
    # Find all .tex files
    tex_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    
    print(f"Found {len(tex_files)} .tex files")
    
    total_replacements = 0
    
    for tex_file in tex_files:
        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix paths in includegraphics commands
            for old_folder, new_folder in folder_mapping.items():
                # Pattern: {old_folder/filename} -> {new_folder/filename}
                pattern = r'\{' + re.escape(old_folder) + r'/'
                replacement = '{' + new_folder + '/'
                content = re.sub(pattern, replacement, content)
                
                # Also fix paths that include the full workspace path
                workspace_pattern = r'\{MainBook_v120250308_014502_3/' + re.escape(old_folder) + r'/'
                workspace_replacement = '{' + new_folder + '/'
                content = re.sub(workspace_pattern, workspace_replacement, content)
            
            # Special case: BoltzmannBrain images being used in other chapters
            # Many chapters are incorrectly referencing BoltzmannBrain images
            # Let's check if the file is not in the BoltzmannBrain folder itself
            if '34_BoltzmannBrain' not in tex_file:
                # Replace BoltzmannBrain references with the correct chapter's image
                content = re.sub(r'\{34_BoltzmannBrain/ChatGPT Image Apr 23, 2025, 01_08_49 PM\.png\}', 
                                '{34_BoltzmannBrain/ChatGPT Image Apr 23, 2025, 01_08_49 PM.png}', content)
            
            if content != original_content:
                with open(tex_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated: {tex_file}")
                total_replacements += 1
        
        except Exception as e:
            print(f"Error processing {tex_file}: {e}")
    
    print(f"\nTotal files updated: {total_replacements}")

if __name__ == "__main__":
    fix_image_paths() 