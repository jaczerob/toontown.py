import ttr
import ttr.models


def main():
    with ttr.SyncToontownClient() as client:
        print(client.doodles())
        print(client.field_offices())
        print(client.invasions())
        # print(client.login(username, password))
        print(client.population())


main()
