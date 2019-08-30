
import os


def dirlist(spider_path, allfile):
    filelist = os.listdir(spider_path)
    for filename in filelist:
        filepath = os.path.join(spider_path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            if filepath.endswith('task.py'):
                allfile.append(filepath)
    return allfile


def get_ktgg_spider_list(base_dir):
    allfile = []
    result = []
    dir_string_list = ['ics', 'task', 'ktgg']
    dir_string = '.'.join(dir_string_list)
    spider_path = os.path.join(base_dir, *dir_string_list)
    dirlist(spider_path, allfile)
    map(lambda x: result.append(split_path(x, dir_string)), allfile)
    return result


def split_path(abs_file_name, dir_string):
    abs_spider_name, _ = os.path.split(abs_file_name)
    _, spider_name = os.path.split(abs_spider_name)
    return '{}.{}.task'.format(dir_string, spider_name)


if __name__ == '__main__':
    base_dir= 'C:\\workspace\\ICS2'
    r = get_ktgg_spider_list(base_dir)
    print r