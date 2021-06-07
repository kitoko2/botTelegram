from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,Update
import requests
import os
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', '8443'))

TOKEN="MON_TOKEN_TELEGRAM"

updater=Updater(token=TOKEN,use_context=True)  # a regler le procces

def start(update,context):
    userName=update["message"]["chat"]["first_name"]
    update.message.reply_text("""
    😎Salut {} tu vas bien j'espere😜!\n
•/time pour voir le temps👀\n
•/youtube pour liens  youtube✨\n 
•/send pour envoyer divers photos de chien(en cours de devellopemnt...)🐱‍🏍\n
•/debut pour lancer le mini menu(en development...)👌
•/blague pour une blague random👌
•/dictionnaire pour rechercher un mots 
""".format(userName))



# def pasconnue(update,context):
#     update.message.reply_text("Commande saisi incorrect")

def time(update,context):
    import time
    t=time.strftime("date: %d/ %m / %Y 😉|😉 heure: %H:%M:%S")
    update.message.reply_text(t)
   
def youtube(update,context):
    update.message.reply_text("www.youtube.com")

def getUrl():
  content=requests.get("https://random.dog/woof.json").json() #pour concertir en json(dictionnaire)# https://poyo200.000webhostapp.com/json/test.json
  print(content)
  urlImage=content['url']

  ext=os.path.splitext(urlImage) #recuperer un tuple qui contient l'extension

  if ext[1]!='.mp4':
      return urlImage

  else:
      return 'null'

  



def send(update,context):
  url=getUrl()
  id_Destinataire= update.message.chat_id #pour l'ID du destinateur
  if url != 'null':
     context.bot.send_photo(chat_id=id_Destinataire,photo=url)
  else:
      update.message.reply_text("erreur reseau, relancer!")


def getBlague():
    r=requests.get("https://www.blagues-api.fr/api/random",headers= {
        'Authorization': 'Bearer [TOKEN_ON_API_BLAGUE]'
        # Bearer [TOKEN]
    })
    if r.status_code==200:
        return r
    else :
        return None

def blague(update,context):
    result=getBlague()
    if result != None:
        result=result.json()
        blague=result["joke"]
        answer=result["answer"]

        update.message.reply_text("{} \n {}😁😁".format(blague,answer))
    else:
        update.message.reply_text("FINI POUR AUJOURD'HUI j'utilise une API gratos donc aider moi en acheter un")


def runDico(update,context):
    update.message.reply_text("entrer un mot a rechercher :")
    updater.dispatcher.add_handler(MessageHandler(Filters.text,entry))
  

   

#use api wikipedia
def entry(update,context):
    name=update['message']['text'] 
    print(name)
    r=requests.get("https://fr.wikipedia.org/w/api.php?action=query&titles={}&prop=extracts&exchars=250&explaintext&utf8&format=json".format(name.lower()))
    if r.status_code==200:
        res=r.json()
        donne=res["query"]["pages"]
        cntDonne=[k for k in donne.keys()]
        page=cntDonne[0]
        if int(page) != -1 :
            update.message.reply_text(res["query"]["pages"][page]["extract"]) #resultat final
        else:
            update.message.reply_text("le mots entrer est introuvale")

updater.dispatcher.add_handler(CommandHandler("send",send))
updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(CommandHandler("youtube",youtube))
updater.dispatcher.add_handler(CommandHandler("time",time))
updater.dispatcher.add_handler(CommandHandler("blague",blague))
updater.dispatcher.add_handler(CommandHandler("dictionnaire",runDico))

# updater.dispatcher.add_handler(MessageHandler(Filters.text,entry))


def debut(update,context):
    keyboard=[
        [InlineKeyboardButton("option1",callback_data="1"),
        InlineKeyboardButton("option2",callback_data="2")],
        [InlineKeyboardButton("option3",callback_data="3")]
    ]

    reply_markup=InlineKeyboardMarkup(keyboard)
    update.message.reply_text("choisis : ",reply_markup=reply_markup)
    
def button(update,context):
    query=update.callback_query
    query.answer() 
    if query.data=="1":
        print("option1")
    if query.data==2:
        print("option2")
    if qyery.data==3:
        print("option3")
    # button sera appeler lorsque un des option /debut sera toucher...

updater.dispatcher.add_handler(CommandHandler("debut",debut))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

# updater.dispatcher.add_handler(MessageHandler(Filters.text,pasconnue))



#pour envoyer une image on a besoin de l'identifiant de l'utilisateur et de l'url




updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN, webhook_url='https://tranquil-tor-69301.herokuapp.com/' + TOKEN)
   
updater.idle()


# updater.bot.set_webhook(url=settings.WEBHOOK_URL)
# remplace updater.start_polling() -> c'est pour travailler en local

# def change(update,context):
#     name=update['message']['text'] #pour avoir acces au text saisir au clavier ( a continuer)
#     update.message.reply_text("changer avec succes")
# def changer_name(update,context):

#     update.message.reply_text("entrer votre nouveau nom :")
#     #a continuer
