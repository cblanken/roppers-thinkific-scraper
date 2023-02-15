import sys
from pathlib import Path
import pandoc
from bs4 import BeautifulSoup 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ./convert.py <course_dir> <out_dir>")
    else:
        course_dir = Path(sys.argv[1])
        out_dir = Path(sys.argv[2])

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

                    
