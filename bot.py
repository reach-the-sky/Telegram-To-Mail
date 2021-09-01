import telebot
import requests

bot = telebot.TeleBot("### telegram key ###")
mailGunApiKey = "### MailGun API Key ###"
domain = "https://api.mailgun.net/v3/### Sandbox Link ###/messages"

# Mail and Help command handling (/Mail, /help).
@bot.message_handler(commands = ["Mail","help"])
def greeting(message):
    bot.send_message(id,"Subject: <Subject> \n <Information> || <Information> || <Image with caption> || <Image>")


# Mail Text Message
def sendMail(subject="Message From ### Your name ###",message=""):
	return requests.post(
		domain,
		auth=("api", mailGunApiKey),
		data={"from": "New Mesage <### From Mail ###>",
			"to": ["### To Mail ###"],
			"subject": subject,
			"text": message})

# Mail with Image
def sendMailWithImage(path,subject="Message From ### Your name ###",message=""):
	return requests.post(
		domain,
		auth=("api", mailGunApiKey),
        files=[("attachment", ("test.jpg", open(path,"rb").read()))],
		data={"from": "New Mesage <### From Mail ###>",
			"to": ["### To Mail ###"],
			"subject": subject,
			"text": message})

# Handling Text Messages
@bot.message_handler(func = lambda x : True)
def receiveMessage(message):
    try:
        if("\n" in message.text):
            temp = message.text.split("\n")
            if("Subject:" in temp[0]):
                sendMail(temp[0].replace("Subject:",""),"".join(temp[1:]))
            else:
                sendMail(message = message.text)
        else:
            sendMail(message = message.text)
        bot.send_message(message.chat.id,"Done")
    except Exception as error:
        bot.send_message(message.chat.id,"Error : "+ str(error))

# Handle Images Chat
@bot.message_handler(func = lambda x : True,content_types=["photo"])  
def receiveImages(message):
    
    # Selecting Largest Image
    file = bot.get_file(message.photo[3].file_id)  
    content = bot.download_file(file.file_path)
    image = open("photo.jpg","wb") 
    
    # Saving Image
    image.write(content) 
    image.close()

    # Start Sending Image
    try:
        # Checking if caption is there
        if(message.caption != None):
            if("\n" in message.caption):
                temp = message.caption.split("\n")
                
                # If there is Subject in the message
                if("Subject:" in temp[0]):
                    sendMailWithImage("photo.jpg",temp[0].replace("Subject:",""),"".join(temp[1:]))
                else:
                    sendMailWithImage("photo.jpg",message = message.caption)
            else:
                sendMailWithImage("photo.jpg",message = message.caption)
        else:
            sendMailWithImage("photo.jpg",message = "No Caption")
        bot.send_message(message.chat.id,"Done")
    except Exception as error:
        bot.send_message(message.chat.id,"Error: " + str(error))

bot.polling()