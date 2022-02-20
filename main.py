from db.PingModal import PingModal

def main():
    
    data = PingModal('users').filter_begining_with('phone_number', '074').count()
    print("Result:", data)
    
if __name__ == '__main__':
    main()