import paramiko
def check_password(client):
        cmd='cat /etc/login.defs | grep "^PASS"'
        stdin,stdout,stderr=client.exec_command(cmd)
        output = stdout.readlines()
        rules = {
                "PASS_MAX_DAYS":("max", 90),
                "PASS_MIN_DAYS":("min", 1),
                "PASS_MIN_LEN":("min", 8),
                "PASS_WARN_AGE":("min", 7)
        }
        for line in output:
                parts=line.split()
                name, value=parts[0], int(parts[1])
                if name in rules:
                        check_type, threshold=rules[name]
                check_rules = (check_type=="max" and value>threshold) or (check_type=="min" and value<threshold)

                if check_rules:
                        print(name,value,"不合格\n" )
                else:
                        print(name,value,"合格\n")

def check_account(client):
        cmd="awk -F: '($2==\"\"){print $1}' /etc/shadow"
        stdin,stdout,stderr=client.exec_command(cmd)
        output=stdout.read().decode()
        print("存在空口令账户",output)

def sign_in_failed(client):
        cmd="grep 'pam_tally2.so' /etc/pam.d/system-auth"
        stdin,stdout,stderr=client.exec_command(cmd)
        output=stdout.read().decode()
        if not output:
                print("未设置登陆失败处理")
        else:
                print(output)

def run(hostname, username, password):
    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, password=password,port=22)
    check_password(client)
    check_account(client)
    sign_in_failed(client)
    client.close()



ip=input("请输入服务器IP: ")
user=input("请输入用户名: ")
password=input("请输入密码: ")
run(ip, user, password)
