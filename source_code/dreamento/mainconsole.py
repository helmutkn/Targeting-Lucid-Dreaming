from source_code.dreamento.scripts.Utils.communicationLogic import CommunicationLogic


def main():
    logic = CommunicationLogic()
    logic.start()


if __name__ == '__main__':
    main()


# TODO:
#   load / import SleePyCo model
#   check if it can handle a single epoch of len == 30 sec
#   make sure the received data is split into 30 sec epochs before feeding the model
#   insert model in HBRecorderInterface
