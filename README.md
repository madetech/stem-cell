# Stem Cell  

## Purpose

To provision a generic AMI that can be used as the basis for numerous specific roles.

## Usage

### Creating the stem cell image

1. Boot an EC2 instance
2. Run ```ansible-playbook stem-cell.yml -u ec2-user```
3. Create an AMI from that instance
4. Terminate the instance

### Using your stem cell AMI

1. In your infrastructure repository, create a main.yml file in the root
2. When creating your EC2 instance provide a JSON object as user-data. Provide an OAuth token (optional) for private repositories.

```json
{
  "version_control_url":"https://github.com/madetech/your-private-repo-here.git",
  "version_control_token":"xxx"
}
```

3. Stem cell will clone the repo and execute the main.yml with ansible

### Example main.yml

```yml
- hosts: localhost
  tasks:
   - name: A very simple task
     file: path=/tmp/test state=touch
```

##Credits

Developed and maintained by [Made Tech](http://www.madetech.co.uk?ref=github&repo=stem-cell).

[![made Tech](https://s3-eu-west-1.amazonaws.com/made-assets/googleapps/google-apps.png)](http://www.madetech.co.uk?ref=github&repo=stem-cell)

Key contributions:

* [Craig J. Bass](https://github.com/craigjbass)

##License

Licensed under [New BSD License](https://github.com/madetech/stem-cell/blob/master/LICENSE)
