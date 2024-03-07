from components.mailer.configs import MailerViewConfig, Mail

def send_email(config:MailerViewConfig, mail: Mail):
    print("\n=== sending mail ===")
    print(f"- URL : {config.queue_url}")
    print(f"- Channel :{config.channel}")
    print(f"- From : {mail._from}")
    print(f"- To : {mail._to}")
    print(f"- Subject : {mail._subject}")
    print(f"- Body : {mail._body}")
    print("======\n")