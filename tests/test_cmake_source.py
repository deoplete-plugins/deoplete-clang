import re
import subprocess

def get_command_help_text(command):
    p = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE)
    return str(p.stdout.read()).replace('\\n', '\n')


def gather_commands():
    help_text= get_command_help_text('cmake --help-commands')
    regex = re.compile(r'\s([\w\d]+\s*\([^)]*?\))')
    commands = regex.findall(help_text)
    all_commands = {}
    for command in commands:
        name = command.split('(')[0].strip()
        if name not in all_commands:
            arg_regex = re.compile(r'\(([^)]*?)\)')
            args = arg_regex.findall(command)[0]
            all_commands[name] = ' '.join(args.replace('\n', ' ').split())
    return all_commands


def gather_variables():
    help_text = get_command_help_text('cmake --help-variable-list')
    language_keyword = ['C', 'CXX', 'FORTRAN', 'JAVA', 'PYTHON']
    all_variables = []
    for variable in help_text.split('\n'):
        if variable.find('<LANG>') >= 0:
            variables = [variable.replace('<LANG>', v)
                    for v in language_keyword]
            all_variables += variables
        elif variable not in all_variables:
            all_variables.append(variable)
    return all_variables


def varify_command(commands):
    normal_commands = [
        'add_compile_options',
        'add_custom_command',
        'add_custom_target',
        'add_definitions',
        'add_dependencies',
        'add_executable',
        'add_library',
        'add_subdirectory',
        'add_test',
        'cmake_minimum_required',
        'cmake_host_system_information',
        'cmake_policy',
        'enable_testing',
        'execute_process',
        'export',
        'file',
        'find_file',
        'find_library',
        'find_package',
        'find_program',
        'find_path',
        'get_cmake_property',
        'get_directory_property',
        'get_target_property',
        'get_test_property',
        'install',
        'if', 'elseif', 'else', 'endif',
        'foreach', 'while', 'endforeach', 'endwhile',
        'function', 'endfunction',
        'message',
        'macro', 'endmacro',
        'option',
        'project',
        'return',
        'set',
        'set_source_files_properties',
        'set_target_properties',
        'set_tests_properties',
        'site_name',
        'source_group',
        'string',
        'target_compile_definitions',
        'target_compile_options',
        'target_include_directories',
        'target_link_libraries',
        'try_compile',
        'try_run',
        'unset',
    ]
    for nc in normal_commands:
        if nc not in commands:
            print(nc,)
            return False
    return True


def varify_varaible(variables):
    common_variables = [
        'CMAKE_BINARY_DIR',
        'CMAKE_COMMAND',
        'CMAKE_CURRENT_BINARY_DIR',
        'CMAKE_CURRENT_LIST_FILE',
        'CMAKE_CURRENT_LIST_DIR',
        'CMAKE_CURRENT_LIST_LINE',
        'CMAKE_CURRENT_SOURCE_DIR',
        'CMAKE_MODULE_PATH',
        'CMAKE_ROOT',
        'CMAKE_SOURCE_DIR',
        'EXECUTABLE_OUTPUT_PATH',
        'LIBRARY_OUTPUT_PATH',
        'PROJECT_NAME',
        'CMAKE_PROJECT_NAME',
        'PROJECT_BINARY_DIR',
        'PROJECT_SOURCE_DIR',
        'CMAKE_INCLUDE_PATH',
        'CMAKE_LIBRARY_PATH',
        'CMAKE_PREFIX_PATH',
        'CMAKE_MAJOR_VERSION',
        'CMAKE_MINOR_VERSION',
        'CMAKE_PATCH_VERSION',
        'CMAKE_TWEAK_VERSION',
        'CMAKE_VERSION',
        'CMAKE_SYSTEM',
        'CMAKE_SYSTEM_NAME',
        'CMAKE_SYSTEM_VERSION',
        'CMAKE_SYSTEM_PROCESSOR',
        'CMAKE_GENERATOR',
        'UNIX',
        'WIN32',
        'APPLE',
        'MINGW',
        'CYGWIN',
        'BORLAND',
        'CMAKE_C_COMPILER_ID',
        'CMAKE_CXX_COMPILER_ID',
        'CMAKE_INCLUDE_CURRENT_DIR',
        'CMAKE_INCLUDE_DIRECTORIES_PROJECT_BEFORE',
        'CMAKE_VERBOSE_MAKEFILE',
        'CMAKE_COLOR_MAKEFILE',
        'BUILD_SHARED_LIBS',
        'CMAKE_AR',
        'CMAKE_BUILD_TYPE',
        'CMAKE_CONFIGURATION_TYPES',
        'CMAKE_C_COMPILER',
        'CMAKE_C_FLAGS',
        'CMAKE_C_FLAGS_DEBUG',
        'CMAKE_C_FLAGS_RELEASE',
        'CMAKE_C_FLAGS_RELWITHDEBINFO',
        'CMAKE_C_OUTPUT_EXTENSION',
        'CMAKE_CFG_INTDIR',
        'CMAKE_CXX_COMPILER',
        'CMAKE_CXX_FLAGS',
        'CMAKE_CXX_FLAGS_DEBUG',
        'CMAKE_CXX_FLAGS_RELEASE',
        'CMAKE_CXX_FLAGS_RELWITHDEBINFO',
        'CMAKE_RANLIB',
        'CMAKE_SHARED_LINKER_FLAGS',
    ]
    for cv in common_variables:
        if cv not in variables:
            print(cv + ' is not found')
            return False
    return True


def main():
    commands = gather_commands()
    if not varify_command(commands):
        print('not all commands are parsed')
        raise Exception
    variables = gather_variables()
    if not varify_varaible(variables):
        print('not all varaibles are found')
        raise Exception

if __name__ == '__main__':
    main()
