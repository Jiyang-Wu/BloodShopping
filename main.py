import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import math

# use creds to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Hackathon").sheet1

# Extract and print all of the values
data = sheet.get_all_records()

Labs = []
lab = ''
while (lab!="No"):
    lab = input("Do you want to add any lab (type No if no more labs are needed):\n")
    Labs.append(lab)
Results = {}
FinalNums = {}
for l in Labs:
    for dic in data:
        if l in dic.values():
            if l in Results.keys():
                Results[l].append([float(dic['Min_collection_volume(mL)']), float(dic['Min_required_volume(mL)']), dic['Color_top']])
            else:
                Results[l]=[[float(dic['Min_collection_volume(mL)']), float(dic['Min_required_volume(mL)']), dic['Color_top']]]

for d in Results.keys():
    for i in Results[d]:
         FinalNums[i[2]] = [0, 0]
for d in Results.keys():
    if len(Results[d])==1:
            FinalNums[Results[d][0][2]][0]+=Results[d][0][0]

            if Results[d][0][1]>FinalNums[Results[d][0][2]][1]:
                 FinalNums[Results[d][0][2]][1] = Results[d][0][1]

for d in Results.keys():
    if len(Results[d])>1:
            ExtraBlood1 = min(Results[d][0][1]-(FinalNums[Results[d][0][2]][1]-FinalNums[Results[d][0][2]][0]),Results[d][0][0])
            ExtraBlood2 = min(Results[d][1][1]-(FinalNums[Results[d][1][2]][1]-FinalNums[Results[d][1][2]][0]),Results[d][1][0])
            if ExtraBlood2>ExtraBlood1:
                FinalNums[Results[d][0][2]][0] += Results[d][0][0]
                if Results[d][0][1] > FinalNums[Results[d][0][2]][1]:
                    FinalNums[Results[d][0][2]][1] = Results[d][0][1]
            else:
                FinalNums[Results[d][1][2]][0] += Results[d][1][0]
                if Results[d][1][1] > FinalNums[Results[d][1][2]][1]:
                    FinalNums[Results[d][1][2]][1] = Results[d][1][1]


for i, j in FinalNums.items():
    if max(j) != 0:
        print(str(max(j))+'mL in the tube type of '+i)






