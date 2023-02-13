import sys
import pandoc
from pathlib import Path

# pandoc.configure(version= '2.19')

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

                    with lesson.open("r") as chapter_contents:
                        html = pandoc.read(file=chapter_contents)
                    
                    with out_file_path.open("w") as out_file:
                        markdown_content = pandoc.write(html, out_file_path, "html", ["--to", "markdown-raw_html-native_divs-native_spans-fenced_divs-bracketed_spans"])


