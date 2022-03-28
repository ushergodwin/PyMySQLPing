from db.PingModel import PingModel
from models.Users import Users
def main():
    
    data = PingModel(Users).objects.count()
    print("Result:", data)
    
if __name__ == '__main__':
    main()