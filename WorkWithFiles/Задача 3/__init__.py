def read_files_info(file_names):
    files_info = []
    for file_name in file_names:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            files_info.append({
                'name': file_name,
                'line_count': len(lines),
                'lines': lines
            })
    return files_info

def merge_files(file_names, output_file):
    files_info = read_files_info(file_names)
    files_info.sort(key=lambda x: x['line_count'])
    
    with open(output_file, 'w', encoding='utf-8') as out:
        for info in files_info:
            out.write(info['name'] + '\n')
            out.write(str(info['line_count']) + '\n')
            out.writelines(info['lines'])
            out.write('\n')

file_names = ['1.txt', '2.txt', '3.txt']
output_file = 'result.txt'

merge_files(file_names, output_file)