import os
import shutil
import uuid
import yaml
import sys
import argparse


def recursively_get_files(dir):
    file_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            file_list.append(os.path.join(root, name))
    return file_list


def get_img_path_list(root_folder):
    img_path_list = recursively_get_files(root_folder)
    return img_path_list


# rename a file with the given path to with uuid
def rename_file_with_uuid(path):
    # os.mv inplace

    fn = os.path.basename(path)
    dirname = os.path.dirname(path)
    age = extract_age_from_fn(fn)
    ext = extract_ext_from_fn(fn)
    uuid_fn = create_uuid_fn(age, ext)
    uuid_path = os.path.join(dirname, uuid_fn)
    shutil.move(path, uuid_path)
    return uuid_path


def extract_age_from_fn(fn):
    """
    :param fn: 'Jeffrey Chen_0040|12.1.jpeg'
    :return: 12.1
    """
    name, ext = os.path.splitext(fn)
    age: str = name.split("|")[-1]
    return age


def extract_ext_from_fn(fn):
    name, ext = os.path.splitext(fn)
    return ext


def create_uuid_fn(age, ext):
    uuid_code = uuid.uuid4().hex
    uuid_fn = uuid_code + "_" + age + ext
    return uuid_fn


def rename_files_with_uuid(path_list):
    return list(map(rename_file_with_uuid, path_list))


def build_mapping(prev_path_list, new_path_list):
    prev_fn_list = path_list2fn_list(prev_path_list, clean_func=replace_space)
    new_fn_list = path_list2fn_list(new_path_list, clean_func=replace_space)
    return dict(zip(prev_fn_list, new_fn_list))


def path_list2fn_list(path_list, clean_func):
    return list(map(lambda path: os.path.basename(clean_func(path)), path_list))

def replace_space(text:str):
    return text.replace(" ", "_")

def move_img_to_folder(img_path, folder):
    basename = os.path.basename(img_path)
    dst_path = os.path.join(folder,basename)
    shutil.move(img_path, dst_path)
    return None


def move_imgs_to_single_folder(img_path_list, dst_folder):
    # map(lambda p: move_img_to_folder(p, dst_folder), img_path_list)
    for p in img_path_list:
        move_img_to_folder(p, dst_folder)
    return None


def write_dict_to_yaml(dict, path):
    with open(path, 'w') as file:
        document = yaml.dump(dict, file)
    return document


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument("--input_dir", "-i", default="img_folder")
    parser.add_argument("--output_dir", "-o", default="dst_folder")
    parser.add_argument("--mapping_fn", "-m", default="fn2uuid.yml")
    args = parser.parse_args(args=argv)

    img_path_list = get_img_path_list(args.input_dir)
    uuid_path_list = rename_files_with_uuid(img_path_list)
    mapping = build_mapping(img_path_list, uuid_path_list)
    write_dict_to_yaml(mapping, args.mapping_fn)
    move_imgs_to_single_folder(uuid_path_list, args.output_dir)

if __name__ == '__main__':
    main(argv=sys.argv[1:])

