import os
import re
import random
import customtkinter as ctk
import google.generativeai as genai
from dotenv import load_dotenv
from tkinter import messagebox

# --- Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

GENRES = ["Cyberpunk", "Fantasy", "Mystery", "Horror", "Post-Apocalyptic", "Historical", "Sci-Fi", "Steampunk", "Supernatural", "Mythological"]
MAX_SEGMENTS = 8
TEXT_FONT = ("Helvetica", 16)
BUTTON_FONT = ("Helvetica", 13)

# --- Story Engine ---
class GeminiStoryGenerator:
    def __init__(self, genres):
        self.genres = genres
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.history = []
        self.segment_count = 0
        self.protagonist = self._generate_protagonist_name()

    def _generate_protagonist_name(self):
        name_bank = {
            "Cyberpunk": ["Nova", "Jax", "Riko", "Zara", "Vex", "Alex"],
            "Fantasy": ["Elira", "Thorne", "Kael", "Aelwyn", "Bran", "Anora"],
            "Mystery": ["Eliot", "Clara", "Detective Wren", "Miles", "Ivy", "Watson"],
            "Horror": ["Ash", "Mara", "Gabe", "Lena", "Silas", "Irelia", "Obediah"],
        }
        return random.choice(name_bank.get(self.genres[0], ["Alex"]))

    def generate_intro(self):
        prompt = f"""You are a world-class short fiction writer. Write an immersive introduction to a short {'/'.join(self.genres)} story featuring the protagonist named {self.protagonist}.

Avoid common tropes like 'data chips', 'shadowy figures', or generic genre bars. Instead, use subtle world-building. Describe unique, genre-blended environments or situations. Set the mood, but do not overwhelm.

Avoid cliches. Avoid overused devices. Be original, clear and immersive.

Format exactly:
INTRO: [your introduction text here]
"""
        try:
            response = self.model.generate_content(prompt)
            intro_match = re.search(r"INTRO:(.*)", response.text, re.DOTALL)
            return intro_match.group(1).strip() if intro_match else "A new world awaits..."
        except Exception as e:
            return f"Error: {e}"

    def _build_prompt(self):
        context = "\n".join(
            f"Chapter {i+1}:\n{entry['segment']}\nChoice: {entry['choice']}"
            for i, entry in enumerate(self.history[-2:])
        )

        twist_bank = {
            "Cyberpunk": [
                "a rogue AI hijacking personal memories",
                "a synthetic dream leaking into reality",
                "a glitch in time tied to cybernetic implants",
                "a black market chip alters personalities",
                "a drone captures forbidden footage of the past",
                "a weather control system malfunctions citywide",
                "virtual reality merges with the real world permanently",
                "a hacker gains sentience mid-hack",
                "corporate implants begin rejecting their hosts",
                "a memory market experiences a data heist",
                "an AI falls in love and disrupts digital networks",
                "city-wide surveillance reveals a ghost identity",
                "augmented citizens start seeing invisible threats",
                "quantum emails appear before they're written",
                "a cybernetic pet carries classified intel",
                "the city's neural net locks everyone out",
                "nanobots rewrite history in real time",
                "a new social score virus resets identities"
            ],
            "Fantasy": [
                "a forbidden spell awakens a slumbering guardian",
                "a mythical creature speaks in forgotten tongues",
                "a prophecy changes mid-reading",
                "a rival claims the same birthmark as the chosen one",
                "a sacred artifact turns out to be a fake",
                "a dying star is visible in daylight",
                "a forest moves to block a kingdom’s army",
                "dragons vanish, leaving only shadows",
                "magic becomes unstable during a blood moon",
                "a crown binds its wearer with ancient voices",
                "a castle appears only when the bell tolls wrong",
                "a ghost king demands a new heir",
                "a well whispers names before someone dies",
                "a sword refuses to be wielded by anyone",
                "a skyship crashes in a land without wind",
                "a village relives the same day until the truth is spoken",
                "an elf finds human memories in their dreams",
                "a royal decree is spoken by animals alone"
            ],
            "Mystery": [
                "a key witness vanishes without a trace",
                "a photograph reveals someone who shouldn't be there",
                "a coded message appears in an old newspaper",
                "the murder weapon was never manufactured",
                "a location keeps appearing in multiple suspects’ dreams",
                "a missing person reappears with no memory of leaving",
                "a sealed room crime scene is bone dry despite flooding",
                "a diary predicts crimes before they happen",
                "the detective is related to every suspect",
                "a note left in invisible ink contradicts all alibis",
                "a grave contains no bones",
                "a film reel loops with new frames each watch",
                "a lock opens without ever being touched",
                "a victim’s blood shows two DNA types",
                "a second moon is visible only to the culprit",
                "all the clocks in the building jump ahead an hour",
                "a lie detector explodes during questioning",
                "the only witness is blind… but describes the killer"
            ],
            "Horror": [
                "a mirror reflects a different reality",
                "a missing person returns... different",
                "a sound only the protagonist can hear",
                "a town that exists only at night",
                "every clock in the area stops at the same time",
                "a child’s drawing predicts future events",
                "a house grows an extra room every day",
                "the shadows whisper warnings to the living",
                "a ritual to banish a spirit summons another",
                "static on a radio tells people's secrets",
                "a skeleton appears wearing tomorrow's clothes",
                "a familiar voice speaks from under the bed",
                "rain causes hallucinations of lost souls",
                "a church bell rings even though it’s gone",
                "furniture rearranges to form words",
                "photos capture people who aren’t there… yet",
                "a voice recorder works with no batteries",
                "the dead leave footprints around the house"
            ],
            "Post-Apocalyptic": [
                "a functioning power grid is discovered underground",
                "a feral child speaks fluent Latin",
                "a mysterious countdown appears in the sky",
                "a message broadcasts in a dead language",
                "a pre-apocalypse structure is untouched and pristine",
                "a river runs backwards for a day",
                "a vaccine causes plants to grow from wounds",
                "moonlight reveals hidden cities underground",
                "a calendar resets itself on its own",
                "a radio station plays only pre-apocalypse ads",
                "a mutated animal mimics human voices",
                "a journal describes the future accurately",
                "robots begin worshipping ancient vending machines",
                "the sky turns red once a week",
                "someone claims to remember the world ending twice",
                "a food ration produces hallucinations of memories",
                "a tree grows where no seeds were planted",
                "a cloud hovers, never moving, above one person"
            ],
            "Historical": [
                "a banned book is found beneath a church",
                "a forgotten heir returns with proof",
                "a sealed letter is decades older than it should be",
                "a noble's portrait subtly changes overnight",
                "a relic bleeds under moonlight",
                "a soldier carries a bullet from the future",
                "a coin shows a monarch that never existed",
                "a journal contradicts known historical events",
                "a tapestry rewrites itself over time",
                "a relic causes nightmares among scholars",
                "a map shows cities that were never built",
                "a statue appears in two locations at once",
                "a play re-enacts future events nightly",
                "a clock tower rings before disaster strikes",
                "a scholar hears voices from the walls of a castle",
                "a duel ends with both sides disappearing",
                "an explorer finds their own bones buried in ruins",
                "a treaty references a war yet to come"
            ],
            "Sci-Fi": [
                "a spacecraft lands but no one exits",
                "a colony receives a signal in their own extinct dialect",
                "gravity reverses for a moment",
                "a stasis pod opens on its own",
                "time skips are reported across multiple galaxies",
                "a black hole behaves like a mirror",
                "teleportation leaves behind echoes",
                "a clone rejects its origin’s identity",
                "a robot begins aging like a human",
                "a meteor writes on the sand in binary",
                "the moon is revealed to be hollow… and awake",
                "alien plants begin reshaping cities overnight",
                "light takes a different path each day",
                "the sun disappears for exactly 37 seconds",
                "a starship crew meets older versions of themselves",
                "quantum entanglement causes déjà vu globally",
                "a time capsule contains an object from tomorrow",
                "a black box records a mission that hasn’t occurred"
            ],
            "Steampunk": [
                "a gearless machine runs endlessly",
                "an automaton paints people’s dreams",
                "a city levitates, then crashes slowly",
                "a mechanical bird sings a banned song",
                "ink made from oil reveals blueprints",
                "steam from factories forms readable shapes",
                "a train with no crew arrives daily",
                "a brass mask reveals true intentions",
                "an airship's compass spins violently before mutiny",
                "a typewriter types confessions on its own",
                "cogs fall from the sky like rain",
                "a monocle sees through solid brass",
                "a clock tower disappears when struck midnight",
                "a new automaton refuses to take orders",
                "a forgotten wrench unlocks a secret lab",
                "steam constructs mimic their creators",
                "a dirigible drifts back with a ghost crew",
                "gears begin turning backwards, time following suit"
            ],
            "Supernatural": [
                "a ghost tries to solve its own murder",
                "a haunted violin plays without strings",
                "a séance summons the wrong spirit",
                "a mirror shows someone else's past",
                "a storm speaks in whispers",
                "possessed graffiti changes daily",
                "a candle burns with memories instead of wax",
                "a black cat lives across centuries",
                "a possessed doll switches its clothes daily",
                "spirits reenact crimes no one knew happened",
                "a priest begins floating during sleep",
                "a haunted house grows a new floor overnight",
                "a wish spoken backwards comes true",
                "a scream echoes in photographs",
                "an invisible friend starts writing letters",
                "dreamcatchers hold real people’s voices",
                "a bell rings for every forgotten soul",
                "shadows detach and move on their own"
            ],
            "Mythological": [
                "a deity wakes up in mortal form",
                "a modern device is found in ancient ruins",
                "a ritual summons the wrong pantheon",
                "a forgotten god demands tribute",
                "a constellation blinks out of the sky",
                "a mortal steals fire... again",
                "Olympus closes its gates without warning",
                "an oracle speaks in tech jargon",
                "a creature of legend applies for asylum",
                "a thunderbolt hits the same place endlessly",
                "a sword hums hymns to the moon",
                "a giant vanishes mid-footstep",
                "a myth changes in real-time as it's read",
                "a hero’s name is erased from every scroll",
                "a demigod refuses their birthright",
                "a labyrinth rebuilds itself every dusk",
                "Mount Olympus is missing from maps",
                "a phoenix rises… as ice"
            ]
        }


        twist_instruction = ""
        if random.random() < 0.5:
            possible_twists = []
            for g in self.genres:
                possible_twists += twist_bank.get(g, [])
            if possible_twists:
                twist_instruction = f"Include: {random.choice(possible_twists)}.\n"

        return f"""
You are a fiction writer generating the next chapter in a {', '.join(self.genres)} story.

Story so far:
{context}

{twist_instruction}
Write the next segment with:
- 1-2 short, immersive paragraphs
- Fresh and unpredictable events (avoid reused phrases like neo-kyoto)
- One event, obstacle, or surprise relevant to the genre
- 2 meaningful and clearly distinct choices (dont make them too big, within 40 words)

Avoid recycled tropes. Be creative, clear, suited for young readers, exciting yet subtle.

Format exactly:
STORY: [story text]
1. [choice 1]
2. [choice 2]
"""

    def _parse_response(self, text):
        story_match = re.search(r"STORY:(.*?)(?=\n\d+\.)", text, re.DOTALL)
        choices = re.findall(r"\d+\.\s*(.*)", text)
        story_text = story_match.group(1).strip() if story_match else "Something strange happens..."
        return {
            "story": story_text,
            "choices": choices[:2] if len(choices) >= 2 else ["Continue", "Look around"]
        }

    def generate_segment(self):
        try:
            prompt = self._build_prompt()
            response = self.model.generate_content(prompt)
            return self._parse_response(response.text)
        except Exception as e:
            return None

    def generate_ending(self):
        context = "\n".join(
            f"Chapter {i+1}:\n{entry['segment']}\nChoice: {entry['choice']}"
            for i, entry in enumerate(self.history)
        )
        prompt = f"""
You are a fiction writer. Based on the story below, write a satisfying ending to a {'/'.join(self.genres)} story.

Story so far:
{context}

The ending should:
- Reflect the protagonist's journey and decisions
- Resolve major tensions or mysteries (not always happily)
- Be genre-consistent
- Be clear, brief (1-2 paragraphs), and original

Format exactly:
ENDING: [your ending here]
"""
        try:
            response = self.model.generate_content(prompt)
            match = re.search(r"ENDING:(.*)", response.text, re.DOTALL)
            return match.group(1).strip() if match else "The story concludes in silence..."
        except Exception as e:
            return f"[Ending error: {e}]"

# --- UI Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Story Generator")
        self.geometry("900x600")

        self.engine = None
        self.current_segment = None
        self.story_active = False

        self._build_layout()

    def _build_layout(self):
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = ctk.CTkFrame(self)
        self.main_area.pack(side="right", expand=True, fill="both")

        self.genre_label = ctk.CTkLabel(self.sidebar, text="Select Genres", font=TEXT_FONT)
        self.genre_label.pack(pady=10)

        self.check_vars = {}
        for genre in GENRES:
            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(self.sidebar, text=genre, variable=var, font=TEXT_FONT)
            cb.pack(anchor="w")
            self.check_vars[genre] = var

        self.start_btn = ctk.CTkButton(self.sidebar, text="Start Story", command=self.start_story, font=BUTTON_FONT)
        self.start_btn.pack(pady=10)

        self.stop_btn = ctk.CTkButton(self.sidebar, text="Stop Story", command=self.stop_story, font=BUTTON_FONT)
        self.stop_btn.pack(pady=5)

        self.quit_btn = ctk.CTkButton(self.sidebar, text="Quit", command=self.destroy, font=BUTTON_FONT)
        self.quit_btn.pack(pady=5)

        self.recap_box = ctk.CTkTextbox(self.sidebar, width=180, height=250, font=TEXT_FONT)
        self.recap_box.pack(pady=10, fill="both", expand=True)
        self.recap_box.insert("end", "Story Recap\n--------------\n")

        self.story_text = ctk.CTkTextbox(self.main_area, font=TEXT_FONT)
        self.story_text.pack(expand=True, fill="both", padx=10, pady=10)

        self.choice_frame = ctk.CTkFrame(self.main_area)
        self.choice_frame.pack(pady=30, fill="x")

        self.choice1_btn = ctk.CTkButton(self.choice_frame, text="", font=BUTTON_FONT, command=lambda: self.make_choice(0))
        self.choice1_btn.pack(pady=10, fill="x", padx=30)

        self.choice2_btn = ctk.CTkButton(self.choice_frame, text="", font=BUTTON_FONT, command=lambda: self.make_choice(1))
        self.choice2_btn.pack(pady=10, fill="x", padx=30)


    def start_story(self):
        selected = [g for g, var in self.check_vars.items() if var.get()]
        if not (1 <= len(selected) <= 2):
            messagebox.showerror("Genre Error", "Select 1-2 genres.")
            return

        self.engine = GeminiStoryGenerator(selected)
        intro = self.engine.generate_intro()
        self.story_text.delete("1.0", "end")
        self.story_text.insert("end", f"🌍 Setting the Scene 🌍\n\n{intro}\n")
        self.recap_box.delete("1.0", "end")
        self.recap_box.insert("end", f"Protagonist: {self.engine.protagonist}\nGenres: {', '.join(selected)}\n")
        self.story_active = True
        self.next_segment()

    def stop_story(self):
        self.story_active = False
        self.story_text.insert("end", "\n🛑 The story has been paused.\n")

    def next_segment(self):
        if not self.story_active:
            return

        if self.engine.segment_count >= MAX_SEGMENTS:
            self.story_text.insert("end", "\n✨ The story ends here...\n")
            ending = self.engine.generate_ending()
            self.story_text.insert("end", f"\n💫 Finale 💫\n{ending}\n")
            self.choice1_btn.configure(state="disabled")
            self.choice2_btn.configure(state="disabled")
            return

        self.current_segment = self.engine.generate_segment()
        if not self.current_segment:
            self.story_text.insert("end", "\n[ERROR generating segment]\n")
            return

        self.story_text.insert("end", f"\n\n📖 Chapter {self.engine.segment_count + 1}\n{self.current_segment['story']}\n")
        self.choice1_btn.configure(text=self.current_segment['choices'][0], state="normal")
        self.choice2_btn.configure(text=self.current_segment['choices'][1], state="normal")

    def make_choice(self, index):
        if not self.story_active:
            return

        choice = self.current_segment['choices'][index]
        self.engine.history.append({
            "segment": self.current_segment['story'],
            "choice": choice
        })
        self.engine.segment_count += 1
        self.recap_box.insert("end", f"\nChapter {self.engine.segment_count}: {choice}")
        self.story_text.insert("end", f"\n👉 You chose: {choice}\n")
        self.next_segment()

if __name__ == "__main__":
    app = StoryApp()
    app.mainloop()
