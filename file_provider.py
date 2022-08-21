import fileinput
import os.path
from os import listdir, mkdir
from functools import wraps

PROJECT_DIRECTORY = ''


class WrongInputException(Exception):
    pass


def retry(error_message: str):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            x = False
            while not x:
                try:
                    return f(*args, **kwargs)
                except WrongInputException:
                    print(error_message)
            return f(*args, **kwargs)
        return f_retry
    return deco_retry


def select_project():
    projects = [x for x in listdir(PROJECT_DIRECTORY) if os.path.isdir(f"{PROJECT_DIRECTORY}/{x}")]
    for ind, p in enumerate(projects):
        print(f"{ind}: {p}")
    selection = input_prompt(len(projects) - 1)
    return projects[selection]


@retry(error_message='That is not a valid project ID')
def input_prompt(number_of_inputs: int):
    project_id = input("Enter corresponding project ID and press enter: ")
    return check_input(project_id, number_of_inputs)


def check_input(input_string: str, number_of_inputs: int):
    try:
        output_string = int(input_string)
    except ValueError as e:
        raise WrongInputException from e
    if output_string > number_of_inputs:
        raise WrongInputException
    return output_string


def check_for_existing_file_provider(file: str):
    with open(file) as f:
        return "<provider" in f.read()


def is_built(directory: str):
    return ".buildozer" in listdir(directory)


def is_xml_dir(directory: str):
    return "xml" in listdir(directory)


def file_paths_xml_exists(directory: str):
    return "file_paths.xml" in listdir(directory)


def manifest_template(project_directory: str):
    app_path = f"{project_directory}/.buildozer/android/platform/build-armeabi-v7a/dists"
    app_name = listdir(app_path)[0]
    template_directory = f"{app_path}/{app_name}/templates"
    if "AndroidManifest.tmpl.xml" in listdir(template_directory):
        return f"{template_directory}/AndroidManifest.tmpl.xml"
    return None


def insert_provider(file: str, file_provider: str):
    file_provider_line = None
    with open(file_provider) as fp:
        with fileinput.FileInput(file, inplace=True) as f:
            for ind, line in enumerate(f):
                if "</receiver>" in line:
                    file_provider_line = ind + 1
                if ind == file_provider_line:
                    line = line.replace(line, f"{line}\n{fp.read()}")
                print(line, end='')


def add_file_paths_xml(file_name: str):
    directory_name = input("Input directory path you wish to access with the file provider: ")
    with open(file_name, "w") as f:
        with open("file_paths.xml", "r") as fp:
            text = fp.read()
            edited_text = text.replace("directory_name", f"app/{directory_name}/")
            edited_text2 = edited_text.replace("directory", directory_name)
            f.write(edited_text2)


def main():
    project = f"{PROJECT_DIRECTORY}/{select_project()}"
    if not is_built(project):
        print("Project hasn't been compiled yet")
        return
    manifest = manifest_template(project)
    if not manifest:
        print("Android Manifest template hasn't been generated")
        return
    provider_exists = check_for_existing_file_provider(manifest)
    if not provider_exists:
        file_provider = 'file_provider.xml'
        insert_provider(manifest, file_provider)
    file_paths_dir = manifest.replace("templates/AndroidManifest.tmpl.xml", "src/main/res")
    if not is_xml_dir(file_paths_dir):
        mkdir(f"{file_paths_dir}/xml")
    if file_paths_xml_exists(f"{file_paths_dir}/xml"):
        print("file_paths.xml already exists")
        return
    file_paths_xml = f"{file_paths_dir}/xml/file_paths.xml"
    add_file_paths_xml(file_paths_xml)


if __name__ == '__main__':
    main()
