## Order of calling hooks in a template

1. pre_fetch() — _runs before downloading sources. Rarely used._
2. do_fetch() — _downloads archives from distfiles. Usually provided by build_style, rarely overridden._
3. post_fetch() — _runs after downloading, before extraction._
4. pre_extract() — _before extracting the archive._
5. do_extract() — _extracts the archive into $wrksrc. Usually from build_style._
6. post_extract() — _after extraction, before applying patches._
7. pre_patch() — _before applying patches from the patches/ directory._
8. do_patch() — _applies patches. Usually from build_style._
9. post_patch() — _after patches, before configuration. Common place for sed edits (like your Hyprland fixes)._
10. pre_configure() — _before running the project’s configuration step (./configure, cmake, etc.)._
11. do_configure() — _runs the configuration command. Usually handled by build_style based on configure_args._
12. post_configure() — _after configuration, before building._
13. pre_build() — _before compilation. Good for tweaking Makefiles or CMake cache._
14. do_build() — _compiles the project (make, cargo build, ninja, etc.). Usually from build_style._
15. post_build() — _after compilation, before tests._
16. pre_check() — _before running tests._
17. do_check() — _runs tests (make check, ctest, cargo test). Often disabled by default._
18. post_check() — _after tests, before installation._
19. pre_install() — _before installing files to ${DESTDIR}._
20. do_install() — _installs files to ${DESTDIR} (via make install, cargo install, etc.). Usually from build_style._
21. post_install() — _final touches for the package: creating runit scripts, copying licenses, removing unwanted files, installing headers/pkgconfig. This is where you use ${PKGDESTDIR} for new files and ${DESTDIR} to adjust already‑installed ones._
22. do_clean() — _cleans up temporary files._

## Порядок вызова хуков в шаблоне:

1. pre_fetch() — _до скачивания исходников. Редко используется._
2. do_fetch() — _скачивает архивы из distfiles. Обычно берётся из build_style, переопределяют редко._
3. post_fetch() — _после скачивания, до распаковки._
4. pre_extract() — _перед распаковкой архива._
5. do_extract() — _распаковывает архив в $wrksrc. Обычно из build_style._
6. post_extract() — _после распаковки, но до патчей._
7. pre_patch() — _перед применением патчей из папки patches/._
8. do_patch() — _применяет патчи. Обычно из build_style._
9. post_patch() — _после патчей, перед настройкой. Тут часто правят файлы через sed, как у тебя с Hyprland._
10. pre_configure() — _перед настройкой проекта (configure/cmake)._
11. do_configure() — _запускает ./configure, cmake и т. п. Обычно из build_style на основе configure_args._
12. post_configure() — _после настройки, перед сборкой._
13. pre_build() — _перед компиляцией. Тут можно, например, подправить Makefile или CMake-кэш._
14. do_build() — _компилирует проект (make, cargo build, ninja). Обычно из build_style._
15. post_build() — _после компиляции, перед тестами._
16. pre_check() — _перед запуском тестов._
17. do_check() — _запускает тесты (make check, ctest, cargo test). По умолчанию часто отключён._
18. post_check() — _после тестов, перед установкой._
19. pre_install() — _перед установкой файлов в ${DESTDIR}._
20. do_install() — _устанавливает файлы в ${DESTDIR} (через make install, cargo install и т. д.). Обычно из build_style._
21. post_install() — _финальная доработка содержимого пакета: создание скриптов (как тот run для runit), лицензий, удаление лишнего, копирование заголовков. Именно тут используют ${PKGDESTDIR} для новых файлов и ${DESTDIR} для доработки уже установленных._
22. do_clean() — _очистка временных файлов._
