import sys
import pandoc
from pathlib import Path
import mdformat

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

                    with lesson.open("r", encoding="utf-8") as chapter_contents:
                        html = pandoc.read(
                            file=chapter_contents,
                            format="html"
                        )
                    
                        # Convert to GitHub-flavored markdown (gfm)
                        markdown_content = pandoc.write(
                            doc=html,
                            file=out_file_path,
                            # format="gfm-raw_html",
                            format="markdown_strict-raw_html",
                        )
