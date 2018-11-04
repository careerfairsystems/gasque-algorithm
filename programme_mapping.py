# -*- coding: utf-8 -*-

desired_programme_guild_mapping = {'F': ['Teknisk Nanovetenskap', 'Teknisk Fysik', 'Teknisk Matematik', 'Engineering Mathematics', 'Engineering Nanoscience', 'Engineering Physics'], 
                                    'E': ['Elektroteknik', 'Medicin och teknik', 'Biomedical Engineering', 'Electrical Engineering'], 
                                    'M': ['Maskinteknik med teknisk design', 'Maskinteknik', 'Mechanical Engineering', 'Mechanical Engineering with Industrial Design'], 
                                    'V': ['Väg- och vatttenbyggnad', 'Lantmäteri', 'Brandingenjörsutbildning', 'Civil Engineering', 'Fire Protection Engineering', 'Surveying'], 
                                    'A': ['Industridesign', 'Architect', 'Industrial Design', 'Arkitekt'], 
                                    'K': ['Kemiteknik', 'Bioteknik', 'Chemical Engineering', 'Biotechnology'], 
                                    'D': ['Datateknik', 'Informations- och kommunikationsteknik', 'Computer Science and Engineering', 'Information and Communication Engineering'], 
                                    'Ing': ['Byggteknik med väg- och trafikteknik', 'Byggteknik med arkitektur', 'Byggteknik med järnvägsteknik', 'Civil Engineering - Architecture', 'Civil Engineering - Railway Construction', 'Civil Engineering- Road and Traffic Technology'], 
                                    'W': ['Ekosystemteknik', 'Environmental Engineering'],
                                    'I': ['Industriell ekonomi', 'Industrial Engineering and Management']}

new_mapping = {}
for key, value in desired_programme_guild_mapping.items():
  print(key + ": " + str(len(value)))
  for v in value:
    new_mapping[v] = key

print(new_mapping)


