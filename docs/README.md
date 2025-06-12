# docusaurus poc

docusaurus quickstart

https://docusaurus.io/docs/3.7.0/category/getting-started

## idea and concept

use the rendered configuration and operation mode command cache

```
make interface_definitions
make op_mode_definitions
```

at the moment the 2 json files will be in a tmp directory. Copy them in the docusaurus root and replace the 2 here.

On docusaurus build. A plugin ```./plugins/docusaurus-plugin-generate-docs``` will preprocess the json files and render the pages from the the command templates in the ```templates``` folder.

Each template must have a yaml header. This header will be used by the render plugin and by docusaurus itself. for example the Title and description field.

```
---
title: VRF
description: VRF Configuration
cfg:
    - vrf
not_cfg:
    - vrf name <tag> protocols
opmode:
    - show vrf
---
```

```cfg``` and ```opmode``` define on which command tree the rendering will start.
```not_cfg``` will exclude and command tree, for example in vrf to have bgp, ospf in the bgp or ospf page.

## build and local server

### local test server

```npx docusaurus start```

### deploy via github

https://docusaurus.io/docs/deployment

https://docusaurus.io/docs/deployment#deploying-to-github-pages


# TODO and open questions

- opmode command cache is not in the final form at the moment
- find a solution for commands which are not a leafnode, for example 'set service ssh' is enough to setup a basic ssh server
- migrate some plugins like "vytask" to a react component https://docusaurus.io/docs/markdown-features/react
- how to deal with versions and translations
    - github branches
    - docusaurus own release implementation https://docusaurus.io/docs/3.7.0/versioning#overview