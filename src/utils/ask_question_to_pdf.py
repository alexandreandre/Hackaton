from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize
from openai import OpenAI
client = OpenAI()

# text="Éric Judor, né le 25 juillet 1968 à Meaux, en France, est l'un des humoristes et acteurs les plus emblématiques de la scène comique française. Ses origines diverses – une mère autrichienne et un père guadeloupéen – ont certainement contribué à la richesse de son univers humoristique. Il grandit dans un environnement multiculturel qui lui permet de développer très tôt une ouverture d’esprit et une curiosité envers différentes cultures et modes de vie. Cet héritage mixte se reflète souvent dans ses œuvres, où il n’hésite pas à jouer avec les stéréotypes pour les déconstruire avec finesse et humour. Avant de devenir une figure incontournable du paysage humoristique français, Éric Judor mène une vie assez éloignée des projecteurs. Après avoir obtenu son baccalauréat, il entreprend des études de commerce international. Cependant, son intérêt pour les langues et les voyages le pousse à explorer de nouvelles horizons. Il travaille alors comme guide touristique aux États-Unis et au Canada, où il perfectionne son anglais et découvre une nouvelle culture qui influencera plus tard son humour. Éric Judor se lance également dans l’aviation civile, devenant brièvement pilote d’avion, une expérience qui souligne son goût pour l’aventure et l’exploration. Le tournant décisif de la vie d’Éric Judor intervient lorsqu’il rencontre Ramzy Bedia en 1994. Leur complicité est immédiate, et ensemble, ils décident de former un duo comique qui va rapidement révolutionner le stand-up en France. Leur style unique, mélange d’absurde, de non-sens, et de satire sociale, trouve un écho particulier chez le public jeune. Ce duo iconique, Éric et Ramzy, commence à se produire dans des cafés-théâtres parisiens, où ils captivent rapidement l’attention des spectateurs par leur énergie débordante et leur humour décalé. Le véritable essor de leur carrière arrive en 1998 avec la création de la série télévisée H sur Canal+. Cette sitcom, qui se déroule dans un hôpital fictif, devient rapidement culte grâce à son humour absurde et ses personnages excentriques. Éric Judor y incarne Aymé Cesaire, un infirmier paresseux et maladroit, tandis que Ramzy joue Sabri Saib, un aide-soignant encore plus déjanté. H permet au duo datteindre une immense popularité, faisant deux des stars de la télévision française. Fort de ce succès, Éric et Ramzy se lancent dans le cinéma. Leur premier film, La Tour Montparnasse Infernale (2001), parodie des films d’action tels que Die Hard. Le film, bien que mal reçu par une partie de la critique, rencontre un grand succès commercial, devenant un film culte pour une génération entière. Ce premier succès est suivi par dautres films comme Double Zéro (2004) et Les Dalton (2004), où le duo continue de développer leur style absurde et burlesque. Malgré le succès en duo, Éric Judor cherche à s’affranchir de cette étiquette et à explorer de nouvelles voies créatives. Il se lance alors dans la réalisation et l’écriture de scénarios, désirant offrir un humour plus personnel et introspectif. En 2007, il réalise Seuls Two, un film dans lequel il explore les thèmes de la solitude et de l’isolement à travers une comédie fantaisiste. Bien que le film ne rencontre pas le succès escompté, il marque une étape importante dans sa carrière, confirmant son désir de se réinventer. En 2012, Éric Judor surprend à nouveau en créant et en interprétant le rôle principal de la série télévisée Platane. Cette série semi-autobiographique met en scène un Éric fictif qui, après un accident de voiture, tente de relancer sa carrière en réalisant un film dramatique. Avec un humour plus acide et une réflexion sur la célébrité et l’échec, Platane montre une facette plus mature et réfléchie de l’artiste, tout en conservant son esprit décalé. Éric Judor continue de se diversifier au fil des ans, assumant des rôles plus variés et explorant de nouveaux formats. Il prête ainsi sa voix à de nombreux films danimation, comme dans Kung Fu Panda (2008) où il double le personnage de Maître Singe. Cette diversification témoigne de sa polyvalence en tant qu’artiste, capable de s’adapter à différents genres et publics. En 2016, Éric revient à la réalisation avec le film Problemos, une comédie satirique qui se moque des communautés autonomes et des dérives de la bien-pensance écologique. Ce film, à la fois drôle et critique, démontre une fois de plus la capacité d’Éric à aborder des sujets contemporains avec une légèreté apparente mais un fond réfléchi. Discret sur sa vie privée, Éric Judor est marié et père de plusieurs enfants. Il a toujours cherché à maintenir une séparation entre sa vie publique et sa vie personnelle, préférant que son travail parle pour lui. Cependant, il nhésite pas à partager ses réflexions sur le monde moderne, souvent avec une pointe dironie. Éric Judor se définit comme un éternel curieux, avide d’apprendre et d’explorer de nouvelles idées. Cette curiosité transparaît dans son travail, où il mélange souvent différentes influences culturelles et artistiques. Pour lui, l’humour est un moyen de questionner le monde, de briser les conventions et d’explorer des vérités souvent cachées sous la surface des apparences. Avec une carrière sétendant sur plus de deux décennies, Éric Judor a indéniablement marqué le paysage de la comédie française. Son style, à la fois absurde et intelligent, a influencé une nouvelle génération de comiques qui voient en lui un modèle d’innovation et de liberté créative. Éric Judor na jamais cessé de repousser les limites du genre comique, refusant de se laisser enfermer dans un style ou un rôle prédéfini. Sa capacité à se réinventer, à explorer de nouveaux territoires tout en restant fidèle à son esprit original, fait de lui une figure incontournable de l’humour français contemporain. Que ce soit à travers ses collaborations avec Ramzy, ses projets solo ou ses incursions dans des genres variés, Éric Judor a prouvé qu'il était bien plus qu'un simple humoriste : il est un créateur, un innovateur, et surtout, un artiste qui na jamais peur de prendre des risques. En résumé, Éric Judor est bien plus quun simple comédien ; il est un pionnier de la comédie moderne en France, un explorateur de l’absurde et un visionnaire dont l’œuvre continuera d’inspirer et de faire rire pour les années à venir."
# qst="Résume ce texte"


def gpt3_completion(question,texte):

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": texte},
        {"role": "user", "content": question}
    ]
    )
    print(texte)
    return(response.choices[0].message.content)
load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def split_text(text, chunk_size=5000):
    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
document = read_pdf(filename)
chunks = split_text(document)

texte = document

def ask_question_to_pdf(question,texte):
    return gpt3_completion(question,texte)

