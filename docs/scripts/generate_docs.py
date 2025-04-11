import json
import os
import yaml
import hashlib
from jinja2 import Environment, FileSystemLoader


# Global parameters for input files
XML_CACHE_FILE = "xml_cache.json"
XML_OP_CACHE_FILE = "xml_op_cache.json"

def flatten_json_cfg(d, commandname='', sep=' '):
    '''
    flatten the json data from cfg tree structure to a flat list of dictionaries
    '''
    return_data = []
    for key, value in d.items():
        if key == 'node_data':
            if value['node_type'] == 'tag':
                commandname = commandname + "<tag>" + sep
            value['commandname'] = commandname.strip()
            return_data.append(value)
        else:
            return_data.extend(flatten_json_cfg(value, commandname + key + sep, sep))
    return return_data


def flatten_json_opmode(commands, commandname='', sep=' '):
    '''
    flatten the json data from opmode tree structure to a flat list of dictionaries
    '''
    return_data = []
    for value in commands:
        new_command = value.copy()
        # remove children from the saved command
        new_command.pop('children')
        #if new_command['type'] == 'tagNode':
        #    node_commandname = commandname + f"<tag>" + sep
        #else:
        node_commandname = f"{commandname}{new_command['name']}{sep}"
        new_command['commandname'] = node_commandname.strip()
        return_data.append(new_command)
        return_data.extend(flatten_json_opmode(value.get("children", []), commandname=node_commandname))
    return return_data


# TODO: set an option to render the command as text or markdown or ...
def render_command(command, env, command_hashtable, template_commands, jinja_template): 
    '''
    render a command as text or markdown
    command_hashtable is the hashtable of the commandnames for the template
    cfg_or_opmode is the name of the section in the template file
    either cfg or opmode

    return a string of the rendered command
    '''

    text = ""
    # TODO change to jinja2
    if command.get('docs', dict()).get('headline', None):
        text += f"# {command['docs']['headline']}\n\n"
        text += f"{command['docs']['text']}\n\n"
    
    if command.get('node_type', None) == 'leaf' or command.get('type', None) == 'leafNode':
        hash = generate_hash(command)
        commandnames = command_hashtable[hash]
        # take only the commandnames that are in the template_commands
        commandnames = [commandname for commandname in commandnames if any(commandname.startswith(template_command) for template_command in template_commands)]

        # Use Jinja2 template for leaf nodes
        template = env.get_template(jinja_template)
        text += template.render(
            cmd=command,
            commandnames=commandnames
        )
        text += "\n\n"
    
    return text


def collect_templates_content():
    '''
    collect all template files in the templates directory
    return a list of a dictionary with the following keys:

    - filepath: the path to the template file
    - content: the content of the template file
    - yaml_header: the loaded yaml header of the template file
    '''
    template_files = []
    for root, _, files in os.walk('templates'):
        for filename in files:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, 'templates')
            content = open(filepath, 'r', encoding='utf-8').read()
            if filename.endswith('.mdx'):            
                template_files.append({
                    'filepath': rel_path,
                    'yaml_header': yaml.safe_load(content.split('---')[1]),
                    'content': content
                })
            if filename.endswith('.yml'):
                save_documentation_file({'filepath': rel_path,}, content)

    return template_files


def generate_hash(command):
    '''
    generate a hash of the command
    return a string of the hash
    '''
    content = command.copy()
    # remove the commandname from the content
    content.pop('commandname')
    return hashlib.sha256(json.dumps(content).encode('utf-8')).hexdigest()


def generate_command_hashtable(data):
    '''
    generate a hashtable of the content per commandname
    to find same content in different commands

    return a dictionary with the hash as key and the list of
    commandnames as value
    '''
    command_hashtable = {}
    for command in data:
        hash = generate_hash(command)
        if hash in command_hashtable:
            command_hashtable[hash].append(command['commandname'])
        else:
            command_hashtable[hash] = [command['commandname']]
    # sort commandnames in the list
    [command_hashtable[hash].sort() for hash in command_hashtable]
    return command_hashtable


def extract_command_for_template(commands, hashtable, template_commands):
    '''
    extracta all commands for a template
    ignore duplicates via hashtable and just add the first occurence
    use the hastable to get all commandnames later in rendering

    return a tuple with the commands for the template and the used commandnames
    '''
    used_commandnames = []
    commands_for_template = []
    for template_command in template_commands:
        for command in commands:
            if command['commandname'].startswith(template_command):
                if command['commandname'] in used_commandnames:
                    continue
                # add command to used_commandnames to prevent duplicates
                commands_for_template.append(command)
                hash = generate_hash(command)
                # add all commandnames for the tempate to used_commandnames from the hashtable
                for commandname in hashtable[hash]:
                    if commandname.startswith(template_command):
                        used_commandnames.append(commandname)               
            
    return commands_for_template, used_commandnames


def save_documentation_file(template_file, content):
    """
    Save new file
    
    template_file: Dictionary containing the template file information
    content: The content to write to the file
    """
    full_path = f"docs/{template_file['filepath']}"
    try:
        # Create all required directories
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Write the content to file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Generated documentation file: {full_path}")
    except Exception as e:
        print(f"Error saving documentation file {full_path}: {str(e)}")
        raise


if __name__ == '__main__':
    print("Starting documentation generation process")
    
    env = Environment(
        loader=FileSystemLoader('scripts'),
        trim_blocks=True,
        lstrip_blocks=True
    )

    data_cfg = json.load(open(XML_CACHE_FILE))
    data_opmode = json.load(open(XML_OP_CACHE_FILE))

    # delete empty node_data object
    data_cfg.pop('node_data')
    data_cfg = flatten_json_cfg(data_cfg)

    # flatten the opmode data
    # data_opmode = flatten_json_opmode(data_opmode)

    # at the moment remove duplicates unless this is fixed in the xml files
    opmode_commandnames = []
    data_opmode_new = []
    for command in flatten_json_opmode(data_opmode):
        if command['commandname'] not in opmode_commandnames:
            opmode_commandnames.append(command['commandname'])
            data_opmode_new.append(command)
    data_opmode = data_opmode_new

    # Sort data by commandname
    data_cfg = sorted(data_cfg, key=lambda x: x['commandname'])
    data_opmode = sorted(data_opmode, key=lambda x: x['commandname'])

    # generate a hashtable of the content per commandname
    cfg_command_hashtable = generate_command_hashtable(data_cfg)
    op_command_hashtable = generate_command_hashtable(data_opmode)

    # get template files
    template_files = collect_templates_content()

    # extract commands for templates
    used_cf_commandnames = []
    used_opmode_commandnames = []
    for template_file in template_files:
        new_content = template_file['content']

        if template_file['yaml_header']['cfg']:
            cfg, used_commandnames = extract_command_for_template(data_cfg, cfg_command_hashtable, template_file['yaml_header']['cfg'])
            used_cf_commandnames.extend(used_commandnames)
            # render commands
            for command in cfg:
                new_content += render_command(command, env, cfg_command_hashtable, template_file['yaml_header']['cfg'], 'cfg.md.j2')

        if template_file['yaml_header']['opmode']:
            opmode, used_commandnames = extract_command_for_template(data_opmode, op_command_hashtable, template_file['yaml_header']['opmode'])
            used_opmode_commandnames.extend(used_commandnames)
            # render template
            new_content += "## Operational Mode Commands\n\n"
            for command in opmode:
                new_content += render_command(command, env, op_command_hashtable, template_file['yaml_header']['opmode'], 'opmode.md.j2')
            
        # Save the generated documentation
        save_documentation_file(template_file, new_content)

    print("")
    print("Summary:")
    print(f"- Configuration commands processed: {len(used_cf_commandnames)}")
    print(f"- Operational mode commands processed: {len(used_opmode_commandnames)}")
    print(f"- Total files generated: {len(template_files)}")
