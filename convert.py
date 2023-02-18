import os
import sys
from pathlib import Path
import pandoc
from bs4 import BeautifulSoup 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("""
    $$\        $$\                   $$\            $$\                                  $$\ 
    $$ |       $$ |                  $$ |           \$$\                                 $$ |
    $$$$$$$\ $$$$$$\   $$$$$$\$$$$\  $$ |      $$$$\ \$$\            $$$$$$\$$$$\   $$$$$$$ |
    $$  __$$ \_$$  _|  $$  _$$  _$$\ $$ |      \____| \$$\           $$  _$$  _$$\ $$  __$$ |
    $$ |  $$ | $$ |    $$ / $$ / $$ |$$ |      $$$$\  $$  |          $$ / $$ / $$ |$$ /  $$ |
    $$ |  $$ | $$ |$$\ $$ | $$ | $$ |$$ |      \____|$$  /           $$ | $$ | $$ |$$ |  $$ |
$$\ $$ |  $$ | \$$$$  |$$ | $$ | $$ |$$ |           $$  /        $$\ $$ | $$ | $$ |\$$$$$$$ |
\__|\__|  \__|  \____/ \__| \__| \__|\__|           \__/         \__|\__| \__| \__| \_______|
        """)
        print("Usage")
        print("-------------------------------------------------")
        print("Convert HTML files from <course_dir> into Markdown files in <out_dir>")
        print("$ python ./convert.py <course_dir> <out_dir>")
        print("-------------------------------------------------")
        print("Same as above but re-embed iframe tags at the start of Markdown output file.")
        print("$ EMBED_IFRAME=1 python ./convert.py <course_dir> <out_dir>")
        print("")
    else:
        course_dir = Path(sys.argv[1])
        out_dir = Path(sys.argv[2])

        try:
            EMBED_IFRAME = os.environ["EMBED_IFRAME"] == "1"
        except KeyError:
            EMBED_IFRAME = False

        if EMBED_IFRAME == False:
            print("[!] Warning: <iframe> tags (as well as all those mentioned here -> https://github.github.com/gfm/#disallowed-raw-html-extension-) will be stripped from the markdown output.")
            print("[!] To re-embed <iframe> tags set EMBED_IFRAME=1 in your environment.")

        try:
            for chapter_dir in course_dir.iterdir():
                print(f"- {chapter_dir}")
                for lesson in chapter_dir.iterdir():
                    if lesson.is_file():
                        out_dir_chapter = Path(out_dir, chapter_dir.name)
                        out_dir_chapter.mkdir(parents=True, exist_ok=True)
                        out_file_path = Path(out_dir, chapter_dir.name, f"{lesson.stem}.md")
                        print(f"  - {out_file_path}")

                        with lesson.open("r", encoding="utf-8") as lesson_file:
                            source = lesson_file.read()
                            html = pandoc.read(
                                source=source,
                                format="html+raw_html"
                            )

                            # Convert to GitHub-flavored markdown (gfm)
                            markdown_content = pandoc.write(
                                doc=html,
                                file=out_file_path,
                                format="gfm-raw_html",
                            )

                            # Capture any iframes in source file
                            soup = BeautifulSoup(source, "html.parser")
                            iframes = "\n".join([str(ele) for ele in soup.select("iframe")])

                            # Re-embed iframes
                            with open(out_file_path, "r+") as markdown_file:
                                data = markdown_file.read()
                                markdown_file.seek(0)
                                markdown_file.write(iframes + '\n')
                                markdown_file.write(data)

                            markdown = pandoc.read(
                                file=out_file_path,
                                format="gfm"
                            )

                            pandoc.write(
                                doc=markdown,
                                file=out_file_path,
                                format="markdown_strict"
                            ) 
        except KeyboardInterrupt:
            print("\nStopping conversion...")
