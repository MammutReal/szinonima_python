**Synonym Searcher v0.5**<br/>
Egy magyar szinonimakereső (Python verzió).<br/>

TODO:
- bővített keresés
- lehetőség saját szavak felvételére
- további kötetek feldolgozása (ellentétes jelentésű szavak szótára, szlengszótár)
- adatbázis SQL-be konvertálása
- átírás C++-ra

Használat:<br/>
`python.exe synonym.py`<br/>

> [!TIP]
> A program Qt6-ot használ a guihoz, így a Pyside6 modulra szükség van.<br/>
> A legjobb, ha ehhez virtuális környezetet csinálunk és aktiválunk a program könyvtárában:
> 
> ```
> python.exe -m venv venv
> venv/Scripts/activate.bat
> ```
>
> Ezután installálhatjuk a Pyside6-ot:<br/>
>
> `pip install Pyside6`
