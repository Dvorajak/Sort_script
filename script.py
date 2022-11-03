import os
import io

# Funkce pro seřazení bloků
def SortBlocks(file):

    print("Seskupování bloků...")

    # Převedení zaslaných dat (které mají již navýšené hodnoty o 10) pro lepší funkcionalitu s daty
    fileData = io.StringIO(file)

    # Počáteční hodnoty pro rozdělení jednotlivých bloků
    usedTool = ""
    newTool = ""
    startSave = False

    blocks = {}

    """
    Získá počáteční nástroj reprezentovaný jeho číslem
    Pod tímto číslem začne přidávat jednotlivé řádky do slovníku dokud se číslo nástroje nezmění
    """
    for row in fileData:
        if "X" in row and "Y" in row:

            if "T" in row:
                startSave = True
                newTool = int(row[-3:len(row)])

            if newTool != usedTool and startSave:
                blocks.update({newTool:row})
                usedTool = newTool

            elif newTool == usedTool and startSave:
                blocks[usedTool] += row

    # Počáteční hodnoty pro seskupení bloků
    sortedFile = ""
    fileDatasort = io.StringIO(file)

    CNCData = True
    savedBlocks = False

    """
    Přiřazuje jednotlivé řádky ze zaslaných dat dokud nenarazí na řádek s nástrojem
    Poté vzestupně přiřadí jednotlivé bloky ze slovníku
    """
    for myrow in fileDatasort:

        if "T" in myrow and "X" in myrow and "Y" in myrow:
            CNCData = False

        if CNCData:
            sortedFile += myrow

        elif not savedBlocks:
            for i in range(len(blocks)):
                sortedFile += blocks[i+1]
            savedBlocks = True

        if "$" in myrow and not CNCData:
            sortedFile += "\n" + myrow
            CNCData = True

    return sortedFile

# Funkce na přičtení hodnot o 10
def AddTen(file):

    print("Přičítání souřadnice Y o 10...")

    # Počáteční hodnoty
    openFile = open(file)
    editedFile = ""
    startEdit = False

    """
    Získá číselné souřadnice X a Y
    Jakmile se vyskyne na řádku T započne editace
    """
    for row in openFile:
        if "X" in row and "Y" in row:

            rowLen = len(row)
            findY = row.find("Y")
            endRow = "\n"

            numberX = float(row[1:findY])
            numberY = row[findY+1:rowLen]

            if numberX > 50:

                if "T" in row:
                    numberY = numberY[:numberY.find("T")]
                    endRow = ""
                    startEdit = True

                if startEdit:
                    fnumberY = float(numberY)
                    fnumberY += 10
                    row = row.replace(numberY,str(fnumberY)+endRow)

        editedFile += f"{row}"

    openFile.close()
    return editedFile


# Funkce pro nalezení maximálních a minimálních hodnot
def FindNumbers(file):

    # Převedení zaslaných dat (které mají již navýšené hodnoty o 10 a jsou blokově seřazeny)

    file = io.StringIO(file)

    # Počáteční hodnota a vytvoření prázných listů
    listX = []
    listY = []

    startFinding = False

    """
    Získá číselné hodnoty souřadnice X a Y
    Tyto hodnoty následně připojí do listů
    """
    for row in file:
        if "X" in row and "Y" in row:

            rowLen = len(row)
            findY = row.find("Y")

            numberX = float(row[1:findY])
            numberY = row[findY + 1:rowLen]

            if "T" in row:
                numberY = numberY[:numberY.find("T")]
                startFinding = True

            if startFinding:
                listX.append(numberX)
                listY.append(float(numberY))

    #Vypíše hodnoty
    print(f"-- Max_X: {max(listX)}")
    print(f"-- Min_X: {min(listX)}")
    print(f"-- Max_Y: {max(listY)}")
    print(f"-- Min_Y: {min(listY)}")


# Získá všechny soubory z aktuálního adresáře
dir_list = os.listdir()
find = False

"""
Jestliže načte soubor s koncovkou .i
Zavolá funkce pro přičtení hodnoty a seřazení
Následně se pokusí uložit nový soubor s upravenými daty
"""
for i in dir_list:
    if i.endswith(".i"):

        print(f"\nNačten soubor: {i}")
        newData = AddTen(i)
        newData = SortBlocks(newData)

        find = True

        savedFile = False
        file = (f"{i[:-2]}.txt","x")
        k = 1

        while not savedFile:
            try:
                openFile = open(file[0],file[1])
                openFile.write(newData)
                savedFile = True
                print()
                print(f"Vytvořen nový soubor s úpravou: {file[0]}\n")
                openFile.close()
            except:
                file = f"{i[:-3]}_{k}.txt","x"
                k += 1

        print(f"Maximální a minimální hodnoty:")
        FindNumbers(newData)

# Jestliže nenajde žádný soubor k převední
if not find:
    print("Žádný soubor k převedení nebyl nalezen")

input("\nStiskněte enter pro ukončení")
