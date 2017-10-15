import Database
import telepot

# Messages
USAGE_MESSAGE = "Usage: `/give <user> <amount>` to pay specified user the stipulated amount"
USER_NOT_FOUND = "Either specified user does not exist or is currently not using the bot. Please request for him/her to add @paybob. Forward the following message to him/her:"
NEW_USER_ADD = "{} wants to connect with you on PayBob. Click on this link (t.me/paybobbot) to add PayBob to your telegram."

def give_handler(user_id, arguments):
    # Initialize bot and database helpers
    paybot = telepot.Bot("452146569:AAEdRQMubxBqRpSWYFs931wnUFja8vdHIIQ")
    db = Database.Database()

    # Handle paying
    try:
        payee = arguments[0]
        amount = arguments[1]
        payer = db.getUsername(user_id)
        payee = arguments[0]
        print("Payee " + payee)
        amount = arguments[1]
        print("Amount " + amount)
        description = " ".join(arguments[2:])
        print("Description " + description)
        payee_id = db.getChatID(payee)
        if (len(arguments) < 2):
            paybot.sendMessage(user_id, USAGE_MESSAGE)
        elif (db.getChatID(payee) == None):
            paybot.sendMessage(user_id, USER_NOT_FOUND)
            paybot.sendMessage(user_id, NEW_USER_ADD.format(payer))
        elif(float(amount) > 0):
            db.insertPending(payer, payee, description, amount)
            toAcknowledgeMessage = "To acknowledge {}'s payment of ${}, type `/acknowledge {} {} <description>`".format(payer, amount, payer, amount)
            paybot.sendMessage(payee_id, toAcknowledgeMessage)
            waitingForAcknowledgeMessage = "Waiting for acknowledgement of payment of ${} to {}".format(amount, payee)
            paybot.sendMessage(user_id, waitingForAcknowledgeMessage)
        else:
            paybot.sendMessage(user_id, USAGE_MESSAGE)
    except Exception as e:
        paybot.sendMessage(user_id, USAGE_MESSAGE)
        print(e)