# from srv.libs import utils
import yaml


json_req = {
    "example": {
        "create": {
            "parameters": {
                "name": "example.com",
                "ip": "69.69.69.69"
            }
        }
    }
}

def yaml_parser(file):
    with open(file, 'r') as stream:
        try:
            data = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        else:
            return data


def parser(request):
    sdl_repo = yaml_parser("endpoint.yml")
    for i in request:
        print(i)

parser(json_req)

# def parser():
#     # sdl_repo = utils.repodata()
#     for project in sdl_repo:
#         print(project)