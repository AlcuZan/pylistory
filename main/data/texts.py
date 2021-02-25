"""Module for texts"""
from dataclasses import dataclass

from data.utils import CharName


class Backstories:
    ELIAS = (
        "Elias Holzfeld wurde am 03.07.1906 in Berlin geboren. Er ist jüdischer Herkunft\nund seine Vergangenheit hat ihn "
        "schwer gezeichnet. "
        "Als er noch ein kleiner Junge war, gelangten er und seine Familie im 1. Weltkrieg in Kriegsgefangenschaft. "
        "Seine Mutter überlebte dies nicht. Er verbrachte den Großteil seines Lebens mit "
        "seinem Vater, der nach dem Krieg einen Tischlerbetrieb eröffnete, in dem Elias seine Lehre absolvierte. Der Rest "
        "seiner Familie befindet sich seit dem 1. Weltkrieg auf der Flucht. Ob sie noch leben, weiß Elias nicht. Der "
        "zunehmende Antisemitismus innerhalb der Gesellschaft ist für Elias spürbar, seine Sorge vor einem Umsturz wächst "
        "von Tag zu Tag..."
    )
    KLAUS = (
        "Als Sohn eines Militärarztes und einer Lehrerin wurde Klaus Schneider am 27.11.1900 in Potsdam geboren. Bereits "
        "seit seiner Kindheit wurde ihm vermittelt, dass es wichtige Unterschiede bezüglich Herkunft und Rasse gibt. Während "
        "seiner Schulzeit vertrat er die Überzeugung, der stärkeren Rasse anzugehören und für diese einzutreten. Das "
        "spiegelte sich in seiner politischen Aktivität wider, denn er ist Teil der Sturmabteilung."
        " Seitdem plagen und verfolgen er und seine Kameraden Andersdenkende, politische Gegner und Juden. Mit jedem Opfer "
        "zweifelt Klaus jedoch mehr und mehr an seinen Lebensentscheidungen...ist er wirklich den richtigen Weg gegangen?"
        "Woher kommt der Hass auf das jüdische Volk? Er hat ihn stets eingetrichtert bekommen, aber so langsam kommen Klaus "
        "Zweifel an dem, was er gelernt hat..."
    )


@dataclass
class TextForTextBox:
    text: str
    speaker: str = "narrator"
    done: bool = False


class NarrationTexts:
    INTRO_TEXT_ELIAS = TextForTextBox(
        "Die Auftragslage im Betrieb von Elias' Vater war am Montag ungewöhn-lich hoch gewesen, sodass Elias den Laden "
        "erst sehr spät und ziemlich müde verlassen konnte. Nach einem kurzen Abendessen war er für seine Verhältnisse "
        "sehr früh zu Bett gegangen. Umso verärgerter ist er, dass das heftige Schneetreiben und der Sturm, der Temperaturen "
        "weit unter dem Nullpunkt mit sich bringt, ihn am frühen Morgen des 10. Januar aus dem Schlaf reißt. "
        "Der wilde Wind peitscht gegen das Fenster von Elias in der Zimmerstraße 32. Er steht auf, um das Fenster zu "
        "schließen und wirft dabei nur einen kurzen Blick aus dem Fenster. Draußen sieht er eine Ansammlung von den "
        "Gefolgsleuten Hitlers, wie sie laut grölend eine Kneipe gegenüber verlassen. Elias kennt Männer wie sie - "
        "Mitglieder der Sturmabteilung. Sie gehören zu denen, denen man im Dunkeln lieber nicht begegnen möchte. Elias hört, "
        "wie sie sich über das Treffen im Haus des Bankiers Schröder unterhalten. Sie scheinen freudig darüber zu sein,"
        " dass Hitler und Papen sich darauf einigen konnten, Hitler zum Reichskanzler zu machen. Elias nimmt durch das geöffnete"
        " Fenster auch einige Namen der Anhänger wahr. Einer bleibt ihm besonders im Gedächtnis, denn dieser Mann, welchen sie "
        "Klaus nennen, wirft ihm einen unheilvollen Blick zu, der Elias das Blut in den Adern gefrieren lässt. Schnell schließt "
        "er das Fenster und weicht zurück.",
    )

    INTRO_TEXT_KLAUS = TextForTextBox(
        "Die wachsende Kälte der letzten Wochen hat Klaus und seine Kameraden immer mehr dazu genötigt, "
        "sich am Abend in einer Kneipe Schutz zu suchen. Normalerweise findet man sie eher auf den Straßen. Sie "
        "und der Rest der Sturmabteilung sind dafür verantwortlich, für\nRecht und Ordnung zu sorgen. Doch die "
        "eisigen Temperaturen in dieser Nacht haben den starken Wunsch nach einem wärmenden Getränk verursacht. Als "
        "Klaus einen Blick auf den Kalender an der Wand wirft,\nverrät ihm dieser, dass es bereits der Morgen des "
        "10. Januar ist. Er fordert seine Kameraden zum Gehen auf, da die Pflicht ruft. "
        "Auf dem Weg nach draußen beginnen sie ihr Gespräch über das Treffen im Haus des Bankiers Schröder. "
        "Während seine Kameraden den Gesprächs-verlauf mit immer größer werdender Freude fortführen, wirft Klaus "
        "einen Blick entlang der Fenster der Zimmerstraße. Dort sieht er nur\nkurz den schattenhaften Umriss "
        "eines Mannes, wohlwissend, welche Familien in der Zimmerstraße 32 wohnen. Nach seinem finsteren Blick "
        "zieht sich die Person zurück.",
    )
    FEW_MONTHS_LATER = TextForTextBox(
        "Ein paar Monate später...\n\nSeit der Ernennung Hitlers zum Reichskanzler am 30.01.1933 hat sich viel im Leben "
        "von Elias und Klaus verändert. Elias musste in den letzten Monaten mit ansehen, wie viele Bekannte der Familie "
        "von Hitlers Leuten mitgenommen, geschlagen und teilweise sogar erschossen wurden. Er lebt mit seinem Vater in "
        "ständiger Angst. Die beiden haben gerade Feierabend gemacht und sind zuhause angekommen. \n\n"
        "Klaus hat indes viel mehr Verantwortung zu "
        "tragen. Nach der Machtergreifung Hitlers wurde er Teil der Schutzstaffel. Er ist nun "
        "Scharführer und unter anderem mit der Ausfindigmachung und Deportierung von Juden beauftragt. ",
    )
    KLAUS_MEETS_KREUZER = TextForTextBox(
        "Unterdessen tritt Klaus seinen Kontrollgang an und trifft auf einen seiner Kameraden, welchen er ablöst.",
    )
    ELIAS_WAITS_FOR_ORDER = TextForTextBox(
        "Elias wartet gerade auf die aufgegebene Bestellung, als ein düster aussehender Mann "
        "hereinkommt. Elias erkennt ihn als den Mann, den\ner vor wenigen Monaten vor der "
        "Kneipe gesehen hatte. Der Mann trägt ein braunes Hemd unter der Jacke, "
        "auf dessen linken Arm sich die Kampfbinde befindet, ein rotes Band mit schwarzem "
        "Hakenkreuz in einem weißen Kreis. Beim Anblick dieses Symbols gefriert Elias das "
        "Blut in den Adern. Der Mann kommt auf ihn zu und spricht ihn an."
    )
    ELIAS_AND_KLAUS_GO_TO_DAD = TextForTextBox(
        "Gemeinsam betreten Klaus und Elias das Haus seines Vaters. "
        "Klaus befiehlt Elias, still zu sein."
    )
    ELIAS_HIDES = TextForTextBox("Elias versteckt sich in dem verlassenen Haus.")
    KLAUS_WAITS_IN_FRONT_OF_CARPENTRY = TextForTextBox(
        "Klaus wartet vor der Schreinerei, bis Elias verschwunden ist."
    )
    KLAUS_ENTERS_CARPENTRY = TextForTextBox(
        "Klaus wartet bis die Luft rein ist und betritt die Schreinerei, um die Sachen für Elias zu besorgen."
    )
    KLAUS_LEAVES_CARPENTRY = TextForTextBox(
        "Klaus hat alle Sachen beisammen und macht sich auf zu dem Haus, in das er Elias geschickt hat."
    )
    QUIZ_FAILED = TextForTextBox(
        "Kreuzer nimmt Elias mit ins Konzentrationslager. Klaus kann nur hilflos dabei zusehen..."
    )
    ENDING_EVENT = TextForTextBox(
        "So machen sich Klaus und Elias auf den Weg zur Grenze Richtung Westen, damit Elias fliehen kann."
    )
    ENDING = TextForTextBox(
        "Hier endet der Prototyp von Pylistory. Feedback gerne an manuel_baudach@hotmail.com\n\n"
        "Fortsetzung folgt..."
    )


class Dialogues:
    """Class for dialogue texts. Most of them are properties in the maps, the rest goes here."""

    CLOTHING_CHOSEN_CORRECT = TextForTextBox(
        "Sieht gut aus. Damit sollte dich niemand als Jude erkennen. Lass uns gehen...warte! "
        "Dort vor dem Haus ist mein Kamerad Kreuzer. Er wird dir vermutlich ein paar Fragen stellen."
        "Du musst sie unbedingt richtig beantworten, hörst du?",
        CharName.KLAUS,
    )

    CLOTHING_CHOSEN_INCORRECT = TextForTextBox(
        "Diese Uniform halte ich hier nicht für sinnvoll. Denke daran, sie soll so aussehen wie meine.",
        CharName.KLAUS,
    )
    ELIAS_CANT_PROCEED = TextForTextBox(
        "Da vorne sind Soldaten! In diese Richtung sollte ich nicht laufen...",
        CharName.ELIAS,
    )
    KLAUS_CANT_PROCEED = TextForTextBox(
        "Ich sollte den Kameraden jetzt besser nicht begegnen...", CharName.KLAUS
    )
    KREUZER_WRONG_CHOICE_DEFAULT = TextForTextBox(
        "Falsche Antwort! Ich gebe dir noch eine Chance, Kamerad.", CharName.KREUZER
    )
    KREUZER_WRONG_CHOICE_LAST = TextForTextBox(
        "Falsche Antwort! Du musst noch einiges lernen, Kamerad!", CharName.KREUZER
    )
    KREUZER_TOO_MANY_WRONG_CHOICES = TextForTextBox(
        "Wieder falsch! Ich traue dieser Sache nicht. Das Konzentrationslager ist nicht weit von hier. Herr Scharführer, Sie kennen das Protokoll. Bursche, ich nehme dich mit und überprüfe deine Identität dort.",
        CharName.KREUZER,
    )
    KREUZER_CORRECT_CHOICE_DEFAULT = TextForTextBox(
        "Korrekt! Machen wir weiter.", CharName.KREUZER
    )
    KREUZER_CORRECT_CHOICE_LAST = TextForTextBox(
        "Korrekt! In Ordnung Kamerad, ich denke das reicht. Aus dir kann noch was werden! Danke, dass ich Ihren Schützling testen durfte, Herr Scharführer. Ich schließe mich jetzt wieder der Suche an.",
        CharName.KREUZER,
    )
    KLAUS_LAST_DIALOGUE = TextForTextBox(
        "Gut gemacht Elias. Schnell, wir müssen weg. Richtung Westen! Komm schon!",
        CharName.KLAUS,
    )
    ELIAS_LAST_DIALOGUE = TextForTextBox(
        "In Ordnung, ich komme. Danke Klaus, ohne dich wäre ich verloren...",
        CharName.ELIAS,
    )


class Questions:
    FIRST = "Wann fand die Machtergreifung Hitlers statt?"
    SECOND = "Was wurde beim Treffen zwischen Hitler und Papen im Haus des Bankiers Schröder beschlossen?"
    THIRD = "Wann trat die Verordnung zum Schutz von Volk und Staat in Kraft und was sind wesentliche Inhalte?"
    FOURTH = "An welcher Seite wird die Hakenkreuzbinde getragen?"
    FIFTH = "Welchen Rang willst du einmal erreichen, wenn du so werden willst wie Kamerad Schneider hier?"
