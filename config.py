# Define fields and mappings (unchanged from original code)

fields = [
    "Name",
    "Account number",
    "Last 4 digits of the card",
    "Transaction date",
    "Amount",
    "Merchant name",
    "Date you lost your card",
    "Time you lost your card",
    "Date you realized your card was stolen",
    "Time you realized your card was stolen",
    "When was the last time you used your card",
    "Last transaction amount",
    "Where do you normally store your card",
    "Where do you normally store your PIN",
    "Other items that were stolen",
    "Officer name",
    "Report number",
    "Suspect name",
    "Date",
    "Contact number",
    "Reason for dispute",
    #Add fields as per requirement...
]


checkbox_fields = [
    "Transaction not authorized",
    "My card was",
    "Do you know who made the transaction",
    "Have you given permission to anyone to use your card",
    "Have you filed police report",
    #Add fields as per requirement...
]


field_mappings = {
    "Name" : ["Your Name"],
    "Account number" : ["Account#"],
    "Last 4 digits of the card" : ["Last 4 digits of the card#"],
    "Transaction date" : ["Transaction date"],
    "Amount" : ["Amount$"],
    "Merchant name" : ["Merchant name"],
    "Transaction not authorized" : ["SECTION 1: TRANSACTION NOT AUTHORIZED"], #checkbox entry
    "My card was" : ["My card was (Select one):"], #checkbox entry
    "Date you lost your card"  : ["What DATE did you lose your card?"],
    "Time you lost your card"  : ["What TIME did you lose your card?"],
    "Date you realized your card was stolen"  : ["What DATE did you realize your card was missing?"],
    "Time you realized your card was stolen"  : ["What TIME did you realize your card was missing?"],
    "Do you know who made the transaction" : ["Do you know who made these transactions? (Select one):"], #checkbox entry
    "Have you given permission to anyone to use your card" : ["Have you given permission to anyone to use your card? (Select one):"], #checkbox entry
    "When was the last time you used your card" : ["When was the last time you used your card?","Date:","Time:"],
    "Last transaction amount" : ["Amount: $"],
    "Where do you normally store your card" : ["Where do you normally store your card?"],
    "Where do you normally store your PIN" : ["Where do you normally store your PIN?"],
    "Other items that were stolen" : ["Please list other items that were lost or stolen, including your mobile phone or any', 'additional cards (if applicable):"],
    "Have you filed police report" : ["Have you filed a police report? (Select one)"], #checkbox entry
    "Officer name" : ["District/OWicer name:", "District/OVicer name:"],
    "Report number" : ["Report number:"],
    "Suspect name" : ["Suspect name:"],
    "Date" : ["Date:"],
    "Contact number" : ["Contact number (during the hours of 8am-5pm PST):"],
    "Reason for dispute" : ["Transaction date Amount Merchant Name Reason for dispute"],
    #Add mappings as per requirement...
}
