import os

def join_art_from_files(str_between=''):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file1_path = os.path.join(current_directory, 'ascii_art.txt')
    file2_path = os.path.join(current_directory, 'ascii_art2.txt')

    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        s1 = f1.read()
        s2 = f2.read()

    lines1 = s1.split('\n')
    lines2 = s2.split('\n')
    max_dist = max(len(s) for s in lines1)
    f_str = '{:<'+str(max_dist)+'}{}{}'
    s3 = "\n".join([f_str.format(str1, str_between, str2) for str1, str2 in zip(lines1, lines2)])
    return s3

if __name__ == "__main__":
    combined_art = join_art_from_files(str_between=' |==| ')
    print(combined_art)
