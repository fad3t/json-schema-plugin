# json-schema-plugin

## Usage
```
  [..]
  tasks:
    - name: "validate input against schema"
      json_schema: 
        fatal: true
        instance: "{{ input }}"
        schema: "{{ lookup('file', 'schema.json') }}"
```
