
# SOURCE_INDEX.md

Эта карта источников собрана **под текущую конфигурацию проекта**, а не “вообще по теме”.

Сейчас проект ориентирован на:
- отказ от старой reduced/full architecture как главного пути;
- переход к **mixed-weak criterion** с независимыми окружными каналами `(v,S)` и `(psi,H,chi)`;
- отдельную стабилизацию **осесимметрического background** для полной `simple support` задачи;
- осторожную интерпретацию текущего mixed-weak кандидата на `q_cr`.

Поэтому источники ниже размечены не по “известности статьи”, а по их пользе именно для этой линии.

## Как читать статусы

- **Основной** — можно брать как один из базовых ориентиров при выводе / перепроверке.
- **Основной для интерпретации** — важен для физического смысла и сверки с FEM, но не обязательно даёт финальные формулы.
- **Вспомогательный высокого приоритета** — полезен постоянно, но не должен командовать выводом.
- **Вспомогательный** — источник для сравнений, sanity-check и локальных идей.
- **Навигационный** — нужен, чтобы быстро найти нужную главу/слой теории.

## Рекомендуемый порядок чтения

1. Внутренние документы проекта: `project_journal_updated14.md`, `assumptions.md`, `vyvod_uravneniy_updated17.md`.
2. Осесимметрический фундамент:
   - `notes/chernyh_60_76_axisymmetric_deformation_shell_of_revolution.md`
   - `notes/grigoluk_large_axisymmetric_deflections_shells_of_revolution.md`
   - `notes/makowski_stumpf_1989_finite_axisymmetric_deformation.md`
3. Методика неосесимметрической бифуркации:
   - `notes/huang_1964_unsymmetrical_buckling.md`
   - `notes/cheo_reiss_1973_unsymmetric_wrinkling.md`
4. Линия `simple support` / hinged support / FEM:
   - `notes/bauer_voronkova_semenov_2022_unsymmetric_forms.md`
   - `notes/holm3_asymmetric_buckling_of_circular_and_annular_plates.md`
5. Асимптотические и сравнительные источники:
   - `notes/coman_2016_pressurised_shallow_cap.md`
   - `notes/coman_2013_pressurised_plate_initial_tension.md`
   - `notes/chernyh_150_164_first_approximation_thin_shells.md`
   - `notes/chernyh_165_194_asymptotic_methods.md`

## Карта источников

| PDF | Статус | Для чего открывать | Соответствующая заметка |
|---|---|---|---|
| `Huang 1964 - Unsymmetrical Buckling of Thin Shallow.pdf` | Основной (методика bifurcation) | background → harmonic perturbation → eigenproblem | `notes/huang_1964_unsymmetrical_buckling.md` |
| `bf00534312.pdf` | Основной | общая осесимметрическая геометрия, variational route, критическое равновесие | `notes/makowski_stumpf_1989_finite_axisymmetric_deformation.md` |
| `Chernyh, Kabric, Mihajlovskij, Tovstik, Shamin. Obshchaja n-60-76.pdf` | Основной и приоритетный | осесимметрическая деформация оболочки вращения | `notes/chernyh_60_76_axisymmetric_deformation_shell_of_revolution.md` |
| `Grigoluk-107-147.pdf` | Основной (с ручной верификацией) | большие осесимметричные прогибы / background solver | `notes/grigoluk_large_axisymmetric_deflections_shells_of_revolution.md` |
| `BauerVoronkovaSemenov-vestnik2022_1.pdf` | Основной для интерпретации | hinged/simple-support, FEM vs shallow-shell | `notes/bauer_voronkova_semenov_2022_unsymmetric_forms.md` |
| `holm3.pdf` | Основной для интерпретации | annular/hinged cases, FEM comparison, пределы shallow-shell | `notes/holm3_asymmetric_buckling_of_circular_and_annular_plates.md` |
| `Chernyh, Kabric, Mihajlovskij, Tovstik, Shamin. Obshchaja n-21-40.pdf` | Основной (фундаментальный) | геометрическая база нелинейной теории | `notes/chernyh_21_40_nonlinear_elasticity_basics.md` |
| `Chernyh, Kabric, Mihajlovskij, Tovstik, Shamin. Obshchaja n-41-59.pdf` | Основной | переход от общей теории к оболочке | `notes/chernyh_41_59_shell_reduction_bridge.md` |
| `Chernyh, Kabric, Mihajlovskij, Tovstik, Shamin. Obshchaja n-150-164.pdf` | Основной вспомогательный | что сохраняет/теряет теория первого приближения | `notes/chernyh_150_164_first_approximation_thin_shells.md` |
| `Chernyh, Kabric, Mihajlovskij, Tovstik, Shamin. Obshchaja n-165-194.pdf` | Вспомогательный высокого приоритета | асимптотические режимы и scale arguments | `notes/chernyh_165_194_asymptotic_methods.md` |
| `1_CheoReiss_UnsymmWrinkling_rotated.pdf` | Очень важный вспомогательный | классическая plate-логика wrinkling | `notes/cheo_reiss_1973_unsymmetric_wrinkling.md` |
| `2_Coman_2016-1.pdf` | Вспомогательный высокого приоритета | асимптотика, локализация мод near rim | `notes/coman_2016_pressurised_shallow_cap.md` |
| `3_Coman 2013 - Asymmetric bifurcations in a pressurised.pdf` | Вспомогательный | adjacent equilibrium и edge localisation | `notes/coman_2013_pressurised_plate_initial_tension.md` |
| `BauerVoronkovaRomanova.pdf` | Вспомогательный | plate-level comparison для `p_cr`, `n_cr` | `notes/bauer_voronkova_romanova_loss_of_stability.md` |
| `BauerTovstik.pdf` | Вспомогательный низкого приоритета | другая задача, но полезна по схеме pre-buckling → adjacent equilibrium | `notes/bauer_tovstik_concentrated_load_internal_pressure.md` |
| `1_РИС.9!!!.pdf` | Вспомогательный иллюстративный | FEM-картина переходов и imperfections | `notes/manuylov_kositsyn_begichev_fem_stability.md` |
| `Chernyh, Kabric, Mihajlovskij, Tovstik, Shamin. Obshchaja n-1-20.pdf` | Навигационный | оглавление и карта книги | `notes/chernyh_1_20_frontmatter_navigation.md` |
## Что считать главной опорой проекта сейчас

### 1. Для осесимметрического фона
Главные кандидаты:
- `Chernyh ... n-60-76`
- `Grigoluk-107-147`
- `bf00534312.pdf`

Именно здесь имеет смысл сверять:
- смысл переменных осесимметрической задачи;
- геометрию оболочки вращения;
- BC уровня `simple support`;
- continuation по давлению до bifurcation layer.

### 2. Для неосесимметрической bifurcation logic
Главные источники:
- `Huang 1964 ...`
- `1_CheoReiss_UnsymmWrinkling_rotated.pdf`

Их роль:
- background state → linearized unsymmetric problem;
- harmonic decomposition by wave number;
- eigenvalue/spectral interpretation of critical load.

### 3. Для понимания, почему shallow-level подход может ломаться при hinged support
Главные источники:
- `BauerVoronkovaSemenov-vestnik2022_1.pdf`
- `holm3.pdf`

Их роль:
- support-specific interpretation;
- comparison with FEM;
- прямое предупреждение, что при больших нагрузках и hinged support может понадобиться general shell theory.

## Практическая рекомендация для Codex

Если Codex должен работать над:
- **осесимметрическим background solver’ом** — сначала давай ему заметки по Черныху, Григолюку и Makowski–Stumpf;
- **логикой критерия / bifurcation formulation** — сначала Huang и Cheo–Reiss;
- **интерпретацией simple-support расхождений с FEM** — сначала Bauer 2022 и `holm3`;
- **асимптотическими оценками и mode localisation** — сначала Coman 2016/2013.

## Важная оговорка по сканам

Для нескольких файлов-книг/сканов (`Черных`, `Григолюк`) OCR почти нечитабелен.  
В notes я всё равно отметил их **роль в проекте**, но:
- точные номера формул там нужно при следующем ручном проходе сверять прямо по PDF;
- эти заметки сейчас лучше понимать как **структурные guide-notes**, а не как окончательную формульную выписку.
