# Журнал проекта

## 1. Паспорт проекта

**Тема:**  
Неосесимметрическая потеря устойчивости круглой пластины / оболочки вращения под нормальным давлением: переход от старой reduced/full branch-A архитектуры к новому mixed weak criterion.

**Главная цель:**  
Построить согласованную непологую постановку, в которой:
1. осесимметрический фон вычисляется из исправленной геометрии;
2. линейная задача устойчивости строится на том же фоне без преждевременного устранения окружных каналов;
3. критерий потери устойчивости даёт физически осмысленный минимум по давлению и номеру волны.

**Текущий этап:**  
Старый путь «новый фон + почти та же linearized architecture» исчерпан. Серия тестов (`F_min_reduced`, `F_min_full_v2`, `F_min_full_v3_chernykh`) показала отсутствие qualitative shift: минимум либо уходит к правой границе диапазона давлений, либо критерий становится практически нечувствительным к нагрузке и номеру волны. После этого выполнен переход к новому теоретическому слою: выведен кандидат на **mixed weak criterion** с независимыми окружными каналами `(v,S)` и `(psi,H,chi)`, новой boundary matrix `B_mix(q) ∈ R^{5×2}` и критерием `sigma_min(B_mix(q)) = 0`.

**Критерий завершения текущего этапа:**  
Получить численно воспроизводимую первую mixed-weak реализацию, в которой:
- две central regular modes строятся в новом классе, а не подменяются глобальным ядром surrogate-матрицы;
- правая boundary matrix действительно имеет содержательные строки `u_n(1), varphi(1), T_s(1), S(1), H(1)`;
- `sigma_min(B_mix(q))` даёт качественно новую картину по сравнению со старыми 5D/6D solver’ами.

---

## 2. Ключевые материалы

**Основные файлы:**  
- `vyvod_uravneniy_V15_mixed_weak_criterion.txt` — текущая компактная запись нового mixed weak criterion.  
- `zhurnal_proekta_obnovlennyy13.txt` — этот журнал.  
- `mixed_weak_solver_v1.py` — первая тестовая mixed-weak ветка.  
- `mixed_weak_boundary_matrix_test.py` — первый testbench для настоящей `B_mix`.  
- `mixed_weak_boundary_matrix_test_v2.py` — исправленный testbench с центральной нормировкой двух regular-мод.  
- `fmin_reduced_solver_v1.py`, `fmin_full_solver_v2.py`, `fmin_full_solver_v3_chernykh.py` — зафиксированные отрицательные численные результаты старой архитектуры.  
- `Huang 1964 - Unsymmetrical Buckling of Thin Shallow.pdf` — опорная variational/eigenvalue-логика неосесимметрической потери устойчивости.  
- главы Черныха — опорная геометрия общей теории оболочек.

**Что считать приоритетным при противоречиях:**  
1. Сначала сверяться с `vyvod_uravneniy_V15_mixed_weak_criterion.txt`.  
2. Затем с тем, что реально проверено в testbench’ах и в текущих логах.  
3. После этого — со старыми V11–V14 как с историей предыдущих этапов, а не как с текущей точкой остановки.

---

## 3. Что уже установлено достаточно надёжно

### 3.1. Отрицательные результаты старой архитектуры
- `F_min_reduced` не дал qualitative shift: минимум `sigma_min` по-прежнему уходил к правой границе диапазона давлений.  
- `F_min_full_v2` дал ещё более жёсткий отрицательный результат: критерий почти перестал зависеть от давления и номера волны, лучший `sigma_min` получался при `p=0`.  
- Замена внутреннего блока на `branchA_from_Chernykh` внутри той же full-архитектуры (`F_min_full_v3_chernykh`) практически ничего не изменила по сравнению с `v2`.

**Вывод:** простая замена background и/или частичный ремонт внутреннего оператора внутри старого 5D/6D class **не** создают новый критерий.

### 3.2. Структурный вывод
Проблема не в одной closure-формуле и не в одной строке края, а в том, что старая linearized philosophy слишком рано устраняет окружные каналы. В старой архитектуре отсутствовали независимые пары:
- membrane circumferential layer `(v,S)`;
- twist/shear layer `(psi,H,chi)`.

### 3.3. Новая corrected weak-логика
В качестве нового кандидата зафиксированы:
- corrected kinematics в tangent-normal переменных;
- corrected circumferential bending block;
- новый weak-class с полями  
  `U=(u_s,u_n,v,varphi,psi)` и `P=(T_s,T_theta,S,Q_s,M_s,M_theta,H,chi)`;
- новая right boundary form с парами  
  `(T_s,u_s)`, `(Q_s,u_n)`, `(S,v)`, `(M_s,varphi)`, `(H,psi)`;
- новый mixed weak criterion через `B_mix(q) ∈ R^{5×2}`.

### 3.4. Центр
Principal-part анализ нового weak-класса снова даёт двумерное physical regular family у центра, но это уже **другой** двумерный класс, потому что в него входят независимые окружные каналы.

---

## 4. Текущая формулировка нового критерия

Для фиксированного `n ≥ 2` и давления `q` рассматривается новая weak-постановка
`A_n(X, Xhat; q) = 0`,
где:
- `X=(U,P)`;
- `U=(u_s,u_n,v,varphi,psi)`;
- `P=(T_s,T_theta,S,Q_s,M_s,M_theta,H,chi)`.

У центра существуют две central regular modes
`X_reg^(1)(x)` и `X_reg^(2)(x)`.

Для выбранного типа правой опоры фиксируются существенные условия
- `u_n(1)=0`,
- `varphi(1)=0`,

а свободными остаются
- `u_s(1)`, `v(1)`, `psi(1)`.

Тогда натуральные условия:
- `T_s(1)=0`,
- `S(1)=0`,
- `H(1)=0`.

Следовательно, вводится новая boundary matrix

`B_mix(q) = [[u_n^(1)(1), u_n^(2)(1)],
             [varphi^(1)(1), varphi^(2)(1)],
             [T_s^(1)(1),   T_s^(2)(1)],
             [S^(1)(1),     S^(2)(1)],
             [H^(1)(1),     H^(2)(1)]] ∈ R^{5×2}`.

Новый spectral criterion:
- `sigma_min(B_mix(q)) = 0`.

Именно строки `S(1)` и `H(1)` являются главным формальным отличием нового operator class от старых reduced/full determinant-матриц.

---

## 5. Что уже проверено на новой weak-ветке

### 5.1. Проверка functional-route
- Residual-based weak-form была отбракована: она давала неправильные conjugate pairs на краю.  
- Functional-route через corrected Hellinger–Reissner / modified Reissner оказался рабочим направлением.  
- Выяснилось, что prestress/load block не замыкается в один scalar potential `G(U)`, но естественно существует как **несимметричная билинейная weak-form** `G_ps(U, Uhat)`.

### 5.2. Проверка края
Исправленный functional проходит тест на правую границу: при фиксированных `u_n(1), varphi(1)` и свободных `u_s(1), v(1), psi(1)` автоматически получаются натуральные условия `T_s(1)=0`, `S(1)=0`, `H(1)=0`.

### 5.3. Проверка bulk по `u_s`, `u_n`
Bulk-уравнения по `u_s` и `u_n` восстанавливаются **структурно правильно**; missing piece локализован только в prestress/load-части и больше не размазан по краю, по `(v,S)` или по самой variational philosophy.

---

## 6. Численный статус новой weak-ветки

### 6.1. `mixed_weak_solver_v1.py`
Первая тестовая mixed-weak ветка написана и запускается, но сама по себе ещё не является честной реализацией нового критерия `B_mix`.

### 6.2. `mixed_weak_boundary_matrix_test.py`
Первый testbench для `B_mix` был запущен. Он показал:
- `sigma_Bmix` становится очень малой и убывает с ростом давления;
- но sample `B_mix` почти вырождается в одну строку (`varphi(1)`), а строки `T_s(1), S(1), H(1)` практически зануляются;
- значит, две моды были выбраны неправильно: как глобальное ядро surrogate interior-матрицы, а не как две центрально-нормированные regular-моды.

### 6.3. `mixed_weak_boundary_matrix_test_v2.py`
Подготовлена новая версия testbench, в которой:
- каждая мода строится из центральной нормировки, а не из глобального малого сингулярного вектора;
- для первой моды фиксируется `u_s/x^n = 1`, `phi/x^(n-1)=0`;
- для второй — `u_s/x^n = 0`, `phi/x^(n-1)=1`;
- дополнительно навязаны центральные связи mixed-класса
  `u_n/x^n + (lambda_c/n) phi/x^(n-1) = 0`,
  `psi/x^(n-1) - lambda_c phi/x^(n-1) = 0`.

Эта версия пока **не прогнана пользователем** и является ближайшим обязательным численным тестом.

---

## 7. Что сейчас считается главным открытым местом

Главное открытое место больше не в крае и не в самом факте наличия новых каналов. Теперь оно такое:

**Проверить, заработает ли новая `5×2` boundary matrix как реальный критерий после перехода от глобального surrogate-ядра к двум центрально-нормированным regular-модам.**

Иными словами: нужно отделить
- возможную физическую несостоятельность нового mixed weak class,
от
- чисто численной ошибки первого testbench-а.

---

## 8. Ближайший рабочий план

1. Прогнать `mixed_weak_boundary_matrix_test_v2.py` на диапазоне `0..6 MPa` и модах `n=12,13,14,15`.  
2. Сохранить и сравнить:
   - `sigma_Bmix`,
   - sample `B_mix`,
   - `row norms`,
   - `col norms`,
   - `mode residual norms`.
3. Проверить, перестали ли строки `T_s(1), S(1), H(1)` быть почти нулевыми «по построению».  
4. Если `v2` всё ещё схлопывается к одной строке, не писать сразу следующий solver, а локализовать, на каком шаге теряется новая информация: в центре, в continuation, в правой оценке `H(1)` или в surrogate interior-блоке.  
5. Только после этого решать, стоит ли переходить к полноценной mixed BVP-реализации.

---

## 9. Краткое заключение текущей точки остановки

Старый branch-A/reduced/full путь как основная дорога исчерпан: замена фона и частичный ремонт внутреннего оператора без нового circumferential operator layer качественной смены критерия не дали.

Новый mixed weak criterion теоретически сформулирован достаточно далеко, чтобы начать отдельную тестовую численную ветку. При этом первая boundary-matrix проверка (`v1`) показала не физический ответ, а численную деградацию построения двух мод. Поэтому текущий этап заканчивается не final-формулой для `p_cr`, а переходом к более чистому testbench-уровню:


a) две новые central regular modes уже выделены теоретически;

b) новая boundary matrix `B_mix ∈ R^{5×2}` уже определена;

c) ближайший обязательный шаг — честно проверить `v2`, где эти две моды строятся из центра, а не из глобального surrogate-ядра.


---

## 10. Обновление по mixed-weak численным тестам (текущий зафиксированный итог)

### 10.1. Что было сделано после запуска `mixed_weak_boundary_matrix_test_v2`
1. В `mixed_weak_solver_v1` добавлен bulk-export каналов `S(x), H(x), chi(x)`, так что строки нового класса стали наблюдаемыми не только на правой границе, но и внутри интервала.
2. Для boundary matrix введена диагностическая balanced-версия
   `B_bal = diag(1, 1, 1, 2(1+nu), C_twist) * B_mix`,
   где `gamma_{s theta} = 2(1+nu) S`, `kappa_{s theta} = C_twist H`.
3. Выполнены:
   - широкий scan по давлениям,
   - resolution study,
   - fine scan,
   - adaptive tracking,
   - ultra-fine targeted scan.
4. Диапазон мод был расширен до `n = 10..18`.

### 10.2. Главный численный вывод
На текущий момент наиболее ранний и устойчивый кандидат на начало неосесимметрической потери устойчивости соответствует моде

`n = 13`.

После локального уточнения по давлению и проверки по разрешению получено:

- для `n=13`:
  - `(m_basis, n_collocation) = (16, 420)` -> `p_best = 3.791 MPa`,
  - `(m_basis, n_collocation) = (18, 480)` -> `p_best = 3.794 MPa`.

Отсюда текущий рабочий интервал:

`q_cr^(13) ≈ 3.79..3.80 MPa`.

Для ближайшей конкурирующей ветви:

- для `n=14`:
  - `(16, 420)` -> `p_best = 4.284 MPa`,
  - `(18, 480)` -> `p_best = 4.279 MPa`,

то есть

`q_cr^(14) ≈ 4.28 MPa`.

Следовательно, текущий лучший кандидат на общее критическое давление:

`q_cr ≈ 3.79..3.80 MPa`, `n_cr = 13`.

### 10.3. Как интерпретировать этот результат
Этот результат следует считать **устойчиво локализованным численным кандидатом**, а не окончательно доказанным точным значением, потому что:
- минимальное сингулярное число ещё не достигло машинного нуля;
- значение `sigma_min` в точке минимума остаётся порядка `10^{-7}..10^{-6}`;
- solver/testbench пока остаётся экспериментальной веткой, а не окончательно замкнутой строгой mixed BVP-реализацией.

Тем не менее, для текущего этапа проекта цель достигнута в следующем смысле:
- новая mixed-weak ветка дала качественно новую картину по сравнению со старой reduced/full архитектурой;
- канал `(psi, H, chi)` реально участвует в критерии;
- более раннего кандидата, чем ветка `n=13`, в диапазоне `n=10..18` не найдено.

### 10.4. Что теперь считать главным рабочим утверждением
На текущем этапе проекта считать рабочим утверждением:

> По mixed weak boundary criterion наиболее ранний устойчивый кандидат на начало неосесимметрической потери устойчивости соответствует моде с `13` волнами и лежит в диапазоне `q_cr ≈ 3.79..3.80 MPa`; ближайшая конкурентная ветвь `n=14` лежит около `4.28 MPa`.

### 10.5. Что больше не является главным открытым местом
Больше не считать главным подозреваемым:
- потерю новой информации в центре;
- полное исчезновение каналов `S` и `H` в bulk;
- чисто формальный характер нового mixed-weak класса.


---

## 11. Обновление по separate 6-state simple-support background и continuation architecture

### 11.1. Что теперь фиксировать как текущий статус
Для separate 6-state full-state simple-support background path нужно явно
разделять несколько численных маркеров, а не схлопывать их в один “current
ceiling”:

- канонический old-path anchor/failure pair: `4.3434 / 4.3440 MPa`;
- bounded method-sweep ceiling из pilot 20: `4.3520 MPa` при `u_z`-scaled state;
- bounded audited pilot-21 ceiling: `4.3800 MPa` при `u_z`-scaled continuation + auxiliary arc-like control.

Из этого следует важная интерпретация: старый барьер около `4.344 MPa` больше
нельзя читать как физический потолок ветви. Текущий reading барьера остается
численным и прежде всего conditioning-related, а не как доказанный physical end
of branch.

### 11.2. Что теперь считать preferred workflow
Для высоких нагрузок предпочтительный путь теперь таков:

- базовая formulation: `u_z`-scaled state representation;
- поверх нее: bounded arc-like step adaptation;
- operational split: быстрый checkpointed continuation runner + отдельный
  confirm/audit runner для milestone-точек.

Это не меняет equations и не меняет simple-support BC set. Active mixed-weak
scans при этом по-прежнему не переподключены к honest full-state simple-support
background.

### 11.3. Что уже показал новый fast/confirm слой
Fast/resumable runner уже доведен до `10.0000 MPa` без bounded first failure в
сохраненной лестнице, а short confirm probes прошли через
`10.0200 MPa`.

Для separate simple-support path теперь вводится промежуточный
статус `validated operational milestone`. Он означает high-load point с
сильными same-branch indicators и успешным коротким confirm probe,
но без strict audited-ceiling closure.

По текущим данным:

- `4.4000 MPa` следует читать как validated operational milestone;
- `7.0000 MPa` и `10.0000 MPa` тоже следует читать как validated operational milestones;
- canonical audited ceiling при этом не меняется и остается `4.3800 MPa`.

Это изменение относится только к reporting discipline и не меняет
equations, BCs или physical interpretation. Для следующего `10 -> 15 MPa`
этапа теперь явно фиксируется confirm-critical plan:
`11.0`, `12.0`, `13.0`, `14.0`, `15.0 MPa`, с дополнительными half-step diagnostics
`12.5` и `13.5 MPa`.

---

## 12. Обновление по clean full simple support / подвижный шарнир competition reading и следующему criterion pilot

### 12.1. Что теперь считать текущим clean competition reading
После расширения clean standalone full simple support / подвижный шарнир
search до broad `0..18 MPa` band и после локальных competition checks на
активном наборе мод текущая project-level memory должна быть такой:

- лучший raw minimum сейчас не следует автоматически читать как лучший
  physical candidate;
- текущий лучший **supported** clean candidate соответствует моде `n=6` и
  лежит около `q ≈ 17.6 MPa`;
- мода `n=8` остаётся главным unstable rival: в некоторых локальных окнах она
  даёт более глубокий raw `sigma_bal`, но пока не показала достаточно
  устойчивого superiority reading;
- мода `n=7` даёт sharp raw dips около `17.2..17.4 MPa`, включая dips глубже
  текущего supported candidate, но пока без acceptable robustness и поэтому
  должна оставаться reserve/raw-only mode;
- мода `n=4` по-прежнему полезна как control mode из-за старого
  FEM-oriented prior, но в текущем clean reading остаётся weak branch и не
  апгрейдится в ведущего конкурента.

Все эти значения пока следует описывать как exploratory clean full
simple-support readings, а не как final physical critical load claim.

### 12.2. Что теперь считать главным открытым местом
Для clean full simple support / подвижный шарнир path текущий bottleneck больше
не читается как basic honest-background reach problem. Honest full-state
background уже доведён до широкого operational band, а selected reserve windows
были дополнительно просмотрены выше старого `18 MPa` ceiling neighborhood.

Главное открытое место теперь другое: **criterion discrimination / candidate
selection**. Нужно отделить:

- supported interior valleys,
- window-sensitive unstable rivals,
- raw sharp dips, которые выглядят сильными только по одному числу
  `sigma_bal`.

Именно это, а не прежний background ceiling, теперь является центральным
вопросом clean full simple-support stage.

### 12.3. Какой следующий шаг теперь считать предпочтительным
Pilot `A + C` в текущей форме materially better discrimination не дал.
Branch-aware part оказался полезен в основном отрицательно, а bordered /
augmented solvability reading не дал достаточно устойчивого separation between
`n=6` и `n=8`.

После этого был опробован лёгкий pilot `D` на той же clean architecture:
local tangent-bundle reading, использующий текущие clean blocks
`[A_int(q); B_bal(q)]` и соседние regular subspaces `V_reg`.

Этот первый `D` pilot даёт interior-dominated local signals для `n=6`, `n=7`,
`n=8`, перестаёт делать `n=7` strongest point-like raw dip, но robustly не
закрывает competition between `n=6` и `n=8`; в focused baseline D ranking чаще
лидирует `n=8`.

После этого был отдельно проверен и первый лёгкий pilot `E`: energy-like
reduced-coercivity surrogate на том же local tangent bundle, но уже с
amplitude norm по текущим reconstructed strain / curvature channels.

### 12.4. Что теперь считать резервным / следующим fallback path
`E` оказался полезен diagnostically, но materially competition тоже не закрыл:
reading стал заметно более интерпретируемым и interior-distributed, локальная
window stability для `n=6` и `n=8` улучшилась, но в focused baseline E ranking
всё равно лидирует `n=8`, а `n=7` остаётся competitive.

Следовательно, на project level `n=6` пока остаётся best supported
operational candidate, `n=8` усиливается как methodological rival, а если не
появится более principled reduced-energy construction, следующим шагом должен
быть уже не очередной cheap pilot, а более theoretical criterion rework.

### 12.5. Как теперь фиксировать exact target object criterion rework
Этот более theoretical criterion rework теперь нужно понимать уже не как
абстрактный лозунг, а как конкретный C1/C2 target:

- theorem-level target object на clean full `simple support / подвижный шарнир`
  path нужно фиксировать как full reduced tangent operator на admissible
  center-regular space, а не как один только raw `B_mix`;
- в live clean architecture его текущий конечномерный представитель имеет вид
  `[A_int(q); B_full(q)]`, где boundary rows остаются
  `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`;
- preferred reduced object для следующего proof-oriented шага нужно брать как
  `L_red,n(q) = [A_int(q); B_full(q)] V_adm,n(q)`, где `V_adm` — просто
  center-normalized rebasing того же admissible span, который сейчас задаётся
  `V_reg`;
- raw `B_mix` после этого не удаляется и не отвергается: он остаётся текущим
  baseline reading, но уже как boundary-only descendant более полного reduced
  object;
- ближайшие обязательства после такого freeze: C3 kernel-equivalence step и C4
  решение вопроса, существует ли на том же reduced admissible space genuine
  quadratic-form / second-variation object.

### 12.6. Что реально закрылось в C3, а что осталось открытым
Следующий C3-шаг теперь можно формулировать уже точнее.

- exact kernel-equivalence удалось закрыть только на текущем выбранном
  двумерном reduced family `A_repo = im(V_adm)`: на нём
  `ker(L_red) <-> A_repo ∩ ker(L_full)` через координатное отображение
  `a -> V_adm a`;
- это уже достаточно, чтобы считать `L_red` корректным reduced object именно
  на текущем repo-selected family и чтобы отделить его от чисто boundary-only
  descendants;
- `B_red` и raw `B_mix` теперь нужно понимать как один и тот же
  boundary-only descendant на том же family, только в разных reduced
  координатах;
- при этом два важных вопроса остаются открытыми: совпадает ли `A_repo` с
  полным exact admissible center-regular tangent space clean mixed problem, и
  можно ли вообще честно заменить `L_red` на boundary-only object.

То есть после C3 ближайший обязательный theoretical шаг уже не в том, чтобы
заново «найти объект», а в том, чтобы решить вопрос о losslessness текущего
reduction и только затем переходить к C4 criterion comparison / quadratic-form
decision.

### 12.7. Что C3b уточнил про losslessness
C3b sharpened эту формулировку ещё сильнее.

- current repo-selected family `A_repo = im(V_adm)` теперь уже можно понимать
  не просто как “тот span, который сейчас использует код”, а как exact current
  KKT-selected amplitude family внутри weighted trial ansatz;
- при этом стало явно видно, что `A_repo` не совпадает просто с
  coefficient-level space `ker(C_reg)`: одного current center-regular
  constraints block недостаточно, чтобы получить 2D family;
- значит, текущий theorem-facing bottleneck уже не в том, чтобы лучше описать
  сам selected family, а в том, чтобы доказать, что он действительно exhausts
  full clean admissible center-regular tangent space, а не только current
  ansatz-level construction.

То есть после C3b theorem-level target всё ещё опирается на repo-selected
family, хотя само это family теперь описано существенно точнее и уже не
смешивается с более широким `ker(C_reg)`.

### 12.8. Что дал continuum/local step после C3b
Следующий theorem-facing derivation после C3b дал ещё одно важное уточнение.

- current mixed equations теперь уже поддерживают не только ansatz-level
  two-parameter family, но и local leading-order clean center-regular family в
  current principal center model;
- этот local leading family again parameterized теми же amplitudes
  `(u_s/x^n, varphi/x^(n-1))`, которые current repository использует в `A_ls`;
- однако full local formal-completeness theorem всё ещё не закрыт: frozen
  principal truncation сам по себе не замыкает higher-order local family;
- значит, theorem-level bottleneck сузился ещё сильнее: сначала нужен
  higher-order regular-singular center recurrence step, и только потом можно
  честно решать вопрос `A_full^th = A_ls`.


### 12.9. Что уточнил higher-order recurrence step в fully frozen principal center model
Следующий theorem-facing шаг дал более жёсткий и менее оптимистичный reading,
чем формулировка 12.8 сама по себе.

- previous local two-amplitude statement теперь нужно читать только как
  statement о singular leading block current principal center model;
- если собрать уже полный frozen principal leading layer, то на generic
  nonresonance он forcing'ом зануляет все leading coefficients
  `U0, V0, T0, N0, P0, Y0, M0`;
- после этого next layer не становится full two-amplitude continuation, а даёт
  только one-parameter membrane mode `T1`, при нулевом flexural block;
- checked second layer после подстановки этого membrane mode снова оказывается
  uniquely zero.

Значит, текущий fully frozen principal model не реализует expected clean
local two-amplitude family через проверенные finite orders. Это не опровержение
clean theorem-level target, но это уже явный сигнал, что прежний local-leading
agreement нельзя quietly читать как почти-complete local family.

Project-level consequence теперь такая: следующий обязательный proof-oriented
шаг — не продолжать ту же fully frozen principal truncation, а вернуть первые
omitted finite center coefficients / forcing terms current mixed equations и
уже там выводить richer regular-singular recurrence. Только после этого будет
честно снова спрашивать про local/global completeness и `A_full^th = A_ls`.

### 12.10. Что уточнил C3c richer first-finite center layer
Следующий theorem-facing step показал, что одного only-first-finite repair тоже
недостаточно.

- richer local model действительно возвращает первые honest finite center terms
  current clean background: `c0 = 1 + O(x^2)`, `s0 = K x + O(x^3)`,
  `a0 = 1/x + O(x)`, `lambda_s0 = lambda_c + O(x^2)`,
  `lambda_theta0 = lambda_c + O(x^2)`, `kappa_s0 = K + O(x^2)`,
  `kappa_theta0 = K / lambda_c + O(x^2)`, and the corresponding finite
  prestress / forcing terms;
- но exact order counting now shows that these restored terms start only at
  `O(x^2)` / `O(x^3)` and therefore do not enter the same lowest obstruction
  layer in `R_Ts`, `R_Ms`, and `R_v`;
- consequently the checked richer local model still keeps the same generic
  `P0`-obstruction as the constant-finite layer, so the expected clean
  two-amplitude local family is still not recovered.

Project-level consequence теперь ещё строже: main completeness gap is still
open, and simply “adding the first omitted finite center coefficients” уже не
является достаточным next step. Дальше нужен либо local ingredient, который
может действовать на тех же lowest obstruction orders, либо более точная
reformulation of the theorem-facing local comparison object before снова
спрашивать про `A_full^th = A_ls`.

### 12.11. Что уточнил object-selection step после C3c
Следующий theorem-facing pass сузил reformulation question ещё сильнее.

- live clean code path показывает, что `A_ls = im(M_amp) = im(V_adm)` не просто
  parametrizes current center-regular data, а является unique KKT-selected
  family для задачи
  `min ||A_int c||^2 + reg ||c||^2` при `C_center c = [a1, a2, 0, 0]`;
- значит, current selected family уже несёт hidden weak/interior optimality
  layer, а не только raw local center regularity;
- limited near-center-only surrogate objectives не reproduces тот же selected
  map, so a purely local comparison object is not yet visible in the current
  repository.

Project-level consequence теперь такая:

- direct comparison of `A_ls` with the full unrestricted local center-regular
  family should no longer be treated as the default theorem-facing target;
- the most plausible next target is a **selected** local/germ object: either
  local center-regular family + weak/KKT selection, or local trace of the
  globally weak-selected family already used by the clean code;
- therefore the next immediate theorem-facing step is not another blind local
  coefficient extension, but identification or derivation of that selected
  comparison object.

### 12.12. Что уточнил C3e для local selected object
C3e не закрыл intrinsic local theorem, но sharpened theorem-facing target ещё
сильнее.

- live clean KKT construction теперь удобно читать через selected 4D center-
  data lift `P_sel`, для которого `C_center P_sel = I_4`, а current family
  `A_ls` есть его regularity-zero amplitude slice `im(P_sel D_amp)`;
- это отделяет две разные вещи: center constraints оставляют большой affine
  fiber, а global weak/KKT minimization выбирает внутри него единственный
  selected representative;
- поэтому raw local center-regular family больше не выглядит правильным
  default comparison object for `A_ls`.

Текущий project-level reading теперь такой:

- best exact faithful local object, который уже реально виден на repository
  boundary, есть local trace глобально selected family,
  `A_sel,trace^loc = J_0(A_ls)`;
- purely local intrinsic selector, который воспроизводил бы тот же объект
  inside `A_reg^loc`, пока не найден;
- следующий theorem-facing step должен быть либо global-to-local trace theorem
  for `A_ls`, либо intrinsic characterization theorem for that same selected
  local trace, но уже не blind completeness against the unrestricted local
  family.

### 12.13. Что уточнил C3f для global-to-local trace object
C3f дал более sharp but still conservative result: на current clean boundary
теперь лучше видно не только что `A_ls` is selected, но и что именно считать
its theorem-facing local trace.

- best current theorem-facing meaning of `J_0` is not a full higher-order local
  germ, but the finite leading-center jet `J_0 = C_center` already encoded in
  the live clean ansatz;
- on the current weighted-trial boundary this trace is exact: only the four
  `k = 0` columns of `(u_s, u_n, varphi, psi)` survive in `C_center`, and they
  form an invertible center block;
- therefore `J_0(A_ls)` is now sharply characterized as the basis-independent
  2D selected trace plane `im(D_amp)`, with `J_0|_{A_ls}` uniquely inverted by
  the selected lift `P_sel`.

Project-level consequence now becomes more precise:

- the next comparison object can already be taken to be the selected leading-
  center trace plane `J_0(A_ls)`;
- what remains open is not this finite trace plane itself, but an intrinsic
  higher-order local selected family whose trace would recover the same object;
- so the next immediate theorem-facing step after C3f should be either a
  comparison theorem between the continuum/local selected object and this trace
  plane, or an intrinsic local selected-object theorem that recovers the same
  plane from the full local side.


### 12.14. What C3g clarified for the selected local trace theorem
C3g gave a stronger theorem-facing clarification than just another negative
local observation.

- on the current clean boundary the local comparison object for the selected
  trace stage is now sharp: it should be written in the same coordinates as the
  exact live trace map `J_0 = C_center`, not in an arbitrary local jet
  normalization;
- in these coordinates the singular local compatibility block already recovers
  exactly the same 2D selected trace plane `im(D_amp)` that had been closed
  globally on the weighted-ansatz side;
- so the next comparison object beyond the raw local family is now clear at the
  selected leading-center-trace level.

At the same time, C3g still stays conservative.

- this is not yet a full intrinsic higher-order local selector theorem;
- the exact remaining gap is now sharper: either extend the local theorem to a
  higher-order selected family preserving the same trace plane, or explicitly
  reconcile the current `J_0` coordinates with any alternative richer-local
  trace normalization.


### 12.15. What C3h clarified for the richer local trace
C3h sharpened the next theorem-facing target again.

- the richer local trace should no longer be spoken about as if it were already
  a canonical single object;
- the best current candidate is a truncated regular-singular jet with an
  explicit fourth-coordinate normalization parameter `eta`;
- the already closed selected plane `im(D_amp)` is not expected to appear as the
  same literal zero-defect slice in every such richer chart.

What is now cleanly identified is the invariant core.

- each richer chart carries a 2D lifted selected family;
- there is an explicit triangular projection from that richer trace to the
  canonical current `J_0` coordinates;
- under this projection the lifted family lands exactly on `im(D_amp)`.

So the next immediate theorem-facing step after C3h is no longer vague:
prove a higher-order selected-family theorem for this lifted richer object, not
for an arbitrary chart-dependent zero-defect slice.


### 12.16. What C3i clarified for the first higher-order selected-family step

C3i sharpened the higher-order target again.
The raw lifted 2D selected object from C3h is not exactly preserved by the
first checked post-leading recurrence. What survives is a corrected object: a
one-parameter membrane thickening over that lifted plane.

More precisely, the first checked post-leading recurrence is exactly independent
of the already selected leading amplitudes `(U0, P0)`. Under the same
nonresonance assumption as in the frozen-principal recurrence check, the
post-leading flexural block is rigid, while the membrane block leaves one free
parameter `T1` with visible `U1` and `V1` components. So the next theorem-facing
object is no longer a raw 2D lifted plane, but a corrected lifted family whose
canonical `J_0` projection still equals `im(D_amp)`.

This matters strategically: the next step after C3i should not try to force the
first richer post-leading coefficients back into the old 2D chart. It should
instead identify the intrinsic higher-order rule that either selects,
normalizes, or quotients out this membrane thickening direction while keeping
the same canonical selected leading trace.


### 12.17. What C3j clarified about the membrane thickening direction

C3j refined the higher-order local object once more.
The extra membrane direction from C3i is not presently justified as a canonical
normalization artifact that can simply be set to zero. But it is also not just a
completely amorphous unresolved remainder.

What is now clean is the quotient structure.
The corrected higher-order selected family is 3D, its canonical `J_0`
projection has an exact one-dimensional membrane kernel, and there is a whole
family of 2D sections of that 3D family that all project to the same selected
trace plane `im(D_amp)`. So the current checked local data do not single out one
preferred normalized 2D representative.

Strategically this matters a lot. The next theorem-facing step after C3j should
not be formulated as ?find the right 2D chart? unless an extra intrinsic rule is
first identified. The cleaner target is now: either derive a higher-order rule
that canonically picks a representative of the quotient class, or prove that the
quotient object itself is the final correct local selected object.


### 12.18. What C3k clarified about canonical representatives versus the membrane quotient

C3k sharpened the higher-order local picture again.
The next question after C3j was whether the current checked local equations
already hide a canonical rule that picks one preferred representative of each
membrane-quotient class. The checked answer is still negative.

Several natural candidates were tested, and each fails in a controlled way.
The next checked compatibility layer does not distinguish representatives. The
checked local residual also stays zero along the membrane direction, so local
minimal-residual selection does not help. Conditions like `U1 = 0` are only
chart choices once one allows quotient-preserving coordinate changes. And
orthogonality / minimal-norm rules depend on an extra metric choice, so they do
not yet give an intrinsic local selector.

This is a useful clarification rather than a dead end. The quotient statement is
now stronger: all currently justified local selected invariants factor through
the membrane quotient, and every representative of one quotient class carries
the same canonical selected leading trace plane `im(D_amp)`. So the next
strategy question is no longer just ?find a better 2D chart?. It is more
precise: either derive a genuinely intrinsic higher-order selector, or accept
that the quotient itself is the final correct local selected object.


### 12.19. What C3l decided at the stop-rule fork

C3l closes the local fork on the current checked boundary.
The project no longer needs to keep searching inside the already checked local
data for a hidden canonical 2D representative of the membrane-thickened family.
That search has now been pushed far enough to make a conservative decision.

The decision is Outcome B, but only on the checked boundary.
No intrinsic selector is currently justified there, and every currently checked
local selected invariant factors through the membrane quotient. So the quotient
itself should now be treated as the final local theorem-facing selected object
for the checked local theory.

This is strategically important. The next step is no longer to keep varying
chart normalizations or local minimality rules inside the same checked local
model. The next real advance would have to be one of two things: either a new
intrinsic higher-order selector beyond the current checked boundary, or a
stronger theorem lifting this boundary-scoped quotient finality statement to a
wider local theory.

### 12.20. Quotient-aware return to criterion interpretation

After C3l the local theorem-facing branch is frozen for now at Outcome B on the
current checked boundary. This is a project-strategy stopping point, not a
mathematical impossibility claim about all richer local theories.

The clean criterion story should now be read more sharply:

- `A_ls` remains best read as the global weak/KKT-selected family, not as the
  raw unrestricted local center-regular family;
- `L_red` remains the main theorem-facing reduced object for the clean path;
- `B_red` and `B_mix` remain boundary descendants / coordinate presentations on
  that selected reduced family, operationally useful but not silently upgraded
  into theorem-level substitutes for the full stacked `L_red`;
- the local quotient result adds a stronger caution layer behind the criterion
  reading, but it does not by itself change the clean candidate ordering.

So the current operational competition language stays conservative:

- `n=6` remains the leading supported interior candidate near `17.6 MPa`;
- `n=8` remains the main unstable rival near `17.8 MPa`;
- `n=7` remains a sharp raw reserve dip rather than a supported candidate;
- `n=4` remains a weak control mode.

The immediate next active question is no longer deeper continuation of the same
checked local branch. It is the criterion-level bridge: how the local
Outcome-B quotient result should be read together with the global reduced
criterion objects `A_ls`, `L_red`, `B_red`, and `B_mix` without overclaiming a
final physical criticality theorem.

That next theorem program is now recorded explicitly in
`docs/theory/current_simple_support_theorem_roadmap.md`: the roadmap starts
above the frozen local Outcome-B boundary and treats the global
selected-kernel bridge theorem for `L_red` as the central open target.

### 12.21. T3a implementation stage: finite-dimensional selected-kernel bridge target

The next theorem-facing step is now being organized explicitly as `T3a`, the
first implementable stage inside the broader `T3`, not as a reopening of the
same checked local branch.

The exact repo-level target is:
for fixed clean `(n, q)`, with
`A_sel^repo = A_ls = im(V_adm) = im(M_amp)` on the current weighted-ansatz
boundary and `L_red = [A_int; B_full] V_adm`, selected-class criticality should
be read through the nontrivial-kernel question
`exists 0 != c in A_sel^repo : L_full c = 0`
if and only if
`exists 0 != a in R^2 : L_red a = 0`.

This is still a repository-level selected-class theorem target, not a final
physical criticality theorem. It keeps `B_red` and `B_mix` in their current
descendant/diagnostic role and uses the local Outcome-B quotient result only as
a compatibility constraint on the selected-family reading.

Most of the substance for this finite-dimensional bridge is already present in
repo fragments:

- the selected-family identity
  `A_sel^repo = A_ls = im(V_adm) = im(M_amp)`;
- the reduced-object identity `L_red = [A_int; B_full] V_adm`;
- the bijection `a -> V_adm a` from `R^2` onto `A_sel^repo`;
- the exact restricted-kernel transfer on that class;
- the caution that `B_red` / `B_mix` remain descendants only.

That dedicated `T3a` proof package is now in place through the proof-pilot note
`proof_pilots/pilot_24_t3a_selected_kernel_bridge/pilot_24_t3a_selected_kernel_bridge.md`
together with the existing live helpers
`reduction_check.py` and `selection_object_check.py`.

So on the current repository-selected boundary the finite-dimensional bridge is
now packaged and closed enough: exact theorem statement, exact scope, minimal
lemma split, exact algebra support, and representative live shell checks are
all recorded explicitly. What remains open is not this `T3a` package itself,
but the broader long-term `T3` question beyond the current selected family:
continuum/theorem-facing losslessness, stronger local/global selected-family
comparison, and any later boundary-only collapse theorem.

### 12.22. T3b implementation stage: selected-class upgrade / obstruction beyond T3a

After `T3a`, the next theorem-facing question is no longer the finite-
dimensional kernel transfer on the current repository-selected family. That
part is already closed enough.

The new `T3b` implementation step now goes one stage further than pure
obstruction-staging.
It defines the strongest currently justified theorem-facing candidate class
above the repo-selected family:

`A_sel^{th,cand}
  := { c : J_0(c) in im(D_amp)
       and Q_chk(c) in im(D_rich,eta^corr) / span(g_mem) }`.

So the stronger selected/admissible target is no longer visible only as two
separate shadows. It is now packaged conservatively as one shadow-compatible
candidate class.

The class distinction now has to stay explicit.

- `A_sel^repo` is exact on the current weighted-ansatz boundary and is the
  global weak/KKT-selected family used by the live clean architecture.
- `A_sel^{th,cand}` is the strongest current theorem-facing candidate above that
  family; it keeps exactly the already closed selected trace
  `J_0(A_ls) = im(D_amp)` and the checked local quotient object
  `im(D_rich,eta^corr) / span(g_mem)` as simultaneous admissibility
  conditions.
- this is still not a proof that `A_sel^{th,cand}` is the final intrinsic
  stronger selected class.

The comparison with the repo-selected family is now sharper too:
the strongest currently justified relation is
`A_sel^repo subseteq A_sel^{th,cand}`.
Equality is still open.

So the real remaining gap from `T3a` to long-term `T3` is no longer the bare
construction of a stronger candidate class.
It is the exact comparison/losslessness theorem deciding whether the current
repo-selected family already exhausts `A_sel^{th,cand}` strongly enough to
upgrade the selected-class kernel reading beyond `T3a`.

### 12.23. T3c implementation stage: exact inclusion plus selected-representative obstruction

The next theorem-facing step above the candidate-class package has now been
pushed one stage further too.

The strongest current comparison theorem between the exact repo-selected family
and the stronger candidate class is now:

`A_sel^repo subseteq A_sel^{th,cand}`.

This is exact on the current repository/theory boundary.
But equality is still not closed, and the reason is now sharper than before.

The selected trace and checked local quotient shadows do not currently select a
global representative.

- on the global side, `A_sel^repo = A_ls` is the unique `H = A_int^T A_int + reg I`
  minimal KKT-selected section of a much larger fixed-center fiber;
- on the local checked side, every currently justified selected invariant
  factors through the quotient coordinates, and no checked local condition
  distinguishes representatives inside one quotient class.

So the exact remaining theorem is now clear:
for every `c in A_sel^{th,cand}`, prove or refute the selected-representative
law

`c = P_sel J_0(c)`.

Equivalently, decide whether the candidate class is already exhausted by the
exact repo-selected family.

This is an Outcome-B style comparison result:
exact inclusion is closed enough, exact obstruction to the reverse inclusion is
isolated, but full losslessness is not yet proved and not yet disproved by an
explicit counterexample.

### 12.24. T3d implementation stage: representative law equals selected minimality bridge

The next theorem-facing pass sharpened the same obstruction one level further.

The exact representative law

`c = P_sel J_0(c)`

is no longer just an abstract reverse-inclusion target.
On the current repo-selected boundary it can now be read exactly as a
fiberwise selected-minimality statement:

`c = P_sel J_0(c)` iff `c` is the unique `H = A_int^T A_int + reg I`-minimal
point in its fixed-trace fiber, equivalently iff `z^T H c = 0` for every
fiber direction `z in ker(C_center)`.

This makes the remaining gap much more explicit.

- the trace condition in `A_sel^{th,cand}` fixes only the selected trace
  coordinates in `im(D_amp)`;
- the checked local quotient condition is still representative-lossy on the
  frozen Outcome-B boundary;
- therefore current candidate-class membership does not yet imply the global
  weak/KKT-selected minimality law.

So the exact remaining theorem is now:
prove or refute that every candidate-class element is already fiberwise
`H`-minimal, and hence equal to its exact selected representative
`P_sel J_0(c)`.

This is again an Outcome-B style result:
the representative theorem is not yet proved, but the obstruction is now
identified as one explicit selected-minimality bridge rather than as a generic
comparison gap.

### 12.25. T3e implementation stage: exact fiber-excess functional above the selected representative

The next theorem-facing pass sharpened the same bottleneck one level further
again.

The selected-representative law and the fiberwise `H = A_int^T A_int + reg I`
minimality theorem are now no longer read only through vector orthogonality.
For every shadow-compatible candidate-class element `c`, one can write

`c = P_sel J_0(c) + z`,

with `z in ker(C_center)`, and the current repo-selected representative
`P_sel J_0(c)` is `H`-orthogonal to that fixed-trace fiber.
So the exact identity is

`c^T H c = (P_sel J_0(c))^T H (P_sel J_0(c)) + z^T H z`.

This isolates one explicit nonnegative defect:

`Delta_H(c) := z^T H z = (c - P_sel J_0(c))^T H (c - P_sel J_0(c))`.

Now the remaining theorem can be read in the sharpest current form:

- `Delta_H(c) = 0` iff `c = P_sel J_0(c)`;
- equivalently, `Delta_H(c) = 0` iff `c` is already the unique `H`-minimal
  point in its fixed-trace fiber;
- therefore reverse inclusion and losslessness reduce exactly to proving or
  refuting zero fiber excess on the whole candidate class `A_sel^{th,cand}`.

This is still Outcome B, not a closure theorem.
Current candidate-class membership fixes the selected trace shadow and the
checked local quotient compatibility, but it still does not imply vanishing of
this global fiber-excess functional.

So the next bottleneck is now sharper than in T3d: not merely “prove the
representative law”, but prove or refute

`Delta_H(c) = 0` for every `c in A_sel^{th,cand}`.

### 12.26. T3f implementation stage: shadow-only obstruction and conditional positive-excess template

The next theorem-facing pass pushed the same bottleneck one step further.

The key new point is that the checked local quotient condition is now being used
as an exact lossiness statement rather than as an attempted selector.
On the current checked boundary, every currently justified local selected
invariant factors through the quotient coordinates, and no checked local
condition distinguishes representatives inside one quotient class.

So the candidate class `A_sel^{th,cand}` still controls only:

- the selected leading trace `J_0(c) in im(D_amp)`;
- compatibility with the selected quotient object
  `im(D_rich,eta^corr) / span(g_mem)`.

But it still does not control the representative-level same-trace fiber residue

`z = c - P_sel J_0(c)`.

That sharpens the zero-excess gap.
The exact obstruction is no longer just “`Delta_H(c) = 0` is unproved”.
It is now:

`does there exist a nonzero admissible same-trace, quotient-invisible fiber residual?`

Indeed, if one had

`c_sel in A_sel^repo`

and

`0 != z in A_adm^th intersect ker(C_center)`

such that `c_sel + z` still has checked local shadow in the selected quotient
object, then

`c := c_sel + z`

would lie in `A_sel^{th,cand}` and satisfy

`Delta_H(c) = z^T H z > 0`.

So this gives an exact counterexample template, though not yet an explicit
counterexample.

The active bottleneck after T3f is therefore sharper than after T3e:
prove or refute that no such admissible same-trace, quotient-invisible fiber
residual survives on the current repo/theory boundary.

### 12.27. T3g implementation stage: exact residual-lift class above the T3f shadow-only obstruction

The next theorem-facing pass did not yet prove impossibility of such residuals,
and it did not construct an explicit one either.
But it sharpened the same remaining gap into one exact residual-lift object.

For fixed clean `(n,q)` and a repo-selected representative

`c_sel in A_sel^repo = A_ls = im(V_adm) = im(M_amp)`,

the same-trace residual class is now written exactly as

`R_same,n(q) := ker(C_center,n(q)) = ker(J_0,n(q))`,

and the quotient-invisible admissible lift class is written exactly as

`R_inv,n(q; c_sel)
 := { z in A_adm^th,n(q) intersect R_same,n(q)
      : Q_chk(c_sel + z) = Q_chk(c_sel) }`.

So the T3g question is no longer just
“does some same-trace, quotient-invisible residual survive?”
It is now:

`is R_inv,n(q; c_sel) trivial for every repo-selected representative c_sel?`

This is sharper than T3f because the checked local quotient lossiness is no
longer used only to say that the current candidate class is shadow-only.
It is now used to identify the exact unresolved lift problem.
On the checked local boundary, quotient-invisibility is carried by the local
membrane-kernel line `span(g_mem)`, so the remaining theorem gap is whether
that quotient kernel has any nonzero admissible global lift inside
`ker(C_center)`.

If no such lift exists, then the zero-excess theorem closes and reverse
inclusion follows.
If such a lift exists, then it produces a genuine positive-excess residual
above the same selected trace.

So the status after T3g is still Outcome B, but the open object is now exact:
not an abstract comparison gap, and not merely “prove `Delta_H = 0`”, but
prove or refute triviality of the residual-lift class `R_inv`.

### 12.28. T3h implementation stage: exact kernel/preimage form of the global membrane-lift problem

The next theorem-facing pass did not yet prove impossibility of nonzero global
lifts of the local membrane-kernel line, and it did not construct an explicit
one either.
But it sharpened the T3g residual-lift class into one exact local-to-global
kernel problem.

On the checked local boundary the corrected coefficient quotient map is now
read explicitly as

`q_coeff = [[1,0,0],[0,1,0]]`,

so its kernel is exactly the membrane line

`ker(q_coeff) = span(e_mem)`,

whose jet image is `span(g_mem)`.

For a repo-selected representative `c_sel`, the checked local coefficient
difference of an admissible same-trace global residual `z` is now denoted

`delta_chk,n(q; c_sel)(z)`.

This lets the remaining lift question be written exactly as the global
membrane-lift class

`Lift_mem,n(q; c_sel)
 := { z in A_adm^th,n(q) intersect ker(C_center,n(q))
      : delta_chk,n(q; c_sel)(z) in span(e_mem) }`.

So the old residual class is no longer just a named subset:
on the current linear tangent boundary it is exactly

`Lift_mem,n(q; c_sel) = R_inv,n(q; c_sel)
 = ker(q_coeff o delta_chk,n(q; c_sel))`.

This is the sharpest current theorem-facing reading of the open gap.
The issue is no longer just “is there a quotient-invisible residual?”
It is now:

`does the checked local lift map have nontrivial kernel on the admissible same-trace global residual space?`

So the status after T3h is still Outcome B, but the missing ingredient is
sharper than after T3g:
not merely triviality of a residual class by definition, but explicit control
of the local-to-global map `delta_chk` well enough to decide that kernel.

### 12.29. T3i implementation stage: operator-level obstruction behind the projected lift-map kernel

The next theorem-facing pass did not prove injectivity of the projected checked
local lift map, and it did not produce an explicit nonzero kernel element.
But it sharpened the T3h kernel question one more level.

The exact injectivity object is now written as

`Phi_chk,n(q; c_sel) := q_coeff o delta_chk,n(q; c_sel)`

on the admissible same-trace residual domain

`D_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`,

or, on the checked boundary where the local shadow is actually available, on

`D_res,chk,n(q; c_sel)
 := { z in D_res,n(q) : delta_chk,n(q; c_sel)(z) is defined }`.

So the exact open question is whether

`ker(Phi_chk,n(q; c_sel)) = {0}`.

Since `ker(Phi_chk) = Lift_mem = R_inv`, this is exactly the remaining
zero-excess / reverse-inclusion bottleneck.

The new sharpening is that the obstruction is now operator-level.
On the checked local boundary `q_coeff` is already exact, linear, and
chart-invariant under quotient-preserving chart changes.
So the unresolved piece is no longer the local quotient kernel itself.
It is the absence of an explicit global checked local coefficient-extraction
operator

`chi_chk,n(q)`

on `A_adm^th,n(q) intersect ker(C_center,n(q))` that would make

`delta_chk,n(q; c_sel)(z) = chi_chk,n(q)(z)`

and reduce the kernel question to an ordinary linear injectivity/rank theorem.

So the status after T3i is Outcome D:
the current repo boundary still does not decide injectivity, but the single
exact missing ingredient is now sharper than after T3h, namely explicit
operator-level control of the checked local extraction map on the admissible
same-trace global residual domain.

### 12.30. T3j implementation stage: the local checked extractor is explicit, and the remaining gap is the global shadow bridge

The next theorem-facing pass did not construct a full global operator

`chi_chk,n(q) : D_res,n(q) -> R^3_(a,b,s)`,

but it did sharpen the picture beyond the T3i “missing operator” wording.

On the checked local corrected family

`Xi_sel,corr^(1,eta),n(q) = im(D_rich,eta^corr,n(q))`

there is now an explicit visible-chart linear coefficient extractor

`chi_chk,vis,n(q) = L_vis,n(q)|_(Xi_sel,corr^(1,eta),n(q))`,

with

`L_vis,n(q) D_rich,eta^corr,n(q) = I_3`.

So at the strict checked local corrected-family level the coefficient map is no
longer missing. What remains noncanonical is the full 3-coordinate membrane
representative: under quotient-preserving chart changes the full extractor
changes, but after projection by `q_coeff` the dependence on the chart
disappears exactly.

In fact the projected local extractor is now controlled canonically by the
selected trace:

`q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0`

on `Xi_sel,corr^(1,eta),n(q)`.

So the real remaining gap is now sharper than after T3i:
not “find any local extractor”, but
construct or control a global checked-local shadow map

`Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`

strongly enough that one can compose it with `chi_chk,vis,n(q)` and obtain the
theorem-facing global operator needed for the next injectivity step.

So the status after T3j is Outcome D:
partial construction is available on the strict checked local corrected-family
domain, while the global bridge from admissible same-trace residuals to that
local domain remains the single exact bottleneck.

### 12.31. T3k implementation stage: any compatible raw same-trace shadow already collapses to the zero quotient class

The next theorem-facing pass sharpened the T3j bottleneck again.

It did not construct a full global shadow map

`Sh_chk,n(q) : D_res,n(q) -> Xi_sel,corr^(1,eta),n(q)`,

but it showed that on the current checked boundary this raw target is already
too strong in the wrong direction.

The key exact identity from T3j is

`q_coeff o chi_chk,vis,n(q) = L_amp o Pi_eta_to_J0`

on the checked local corrected family.

Since

`D_res,n(q) = A_adm^th,n(q) intersect ker(C_center,n(q)) subset ker(J_0,n(q))`,

any theorem-facing checked-local shadow map compatible with the current quotient
reading would automatically satisfy

`q_coeff o chi_chk,vis,n(q) o Sh_chk,n(q) = 0`.

So every such raw shadow would have to land in the zero quotient class, hence
in the membrane line `span(g_mem,n(q))`. Equivalently it would amount only to a
scalar membrane-selector candidate

`Sh_chk,n(q)(z) = sigma_chk,n(q)(z) g_mem,n(q)`.

Therefore a raw basepoint-independent factorization of the form

`Phi_chk = q_coeff o chi_chk,vis o Sh_chk`

would be identically zero on `D_res,n(q)` and cannot be the correct remaining
nontrivial bridge.

So the status after T3k is Outcome C:
the missing object is now sharper than after T3j. It is not a raw same-trace
shadow map on `D_res,n(q)`, but a theorem-facing basepoint-relative checked-
local representative-difference object on ambient candidate-class pairs before
quotient collapse, or a theorem that the membrane selector vanishes on the
admissible same-trace residual class.

### 12.32. T3l implementation stage: the surviving checked-local bridge object is the pairwise membrane difference on equal-trace pairs

The next theorem-facing pass followed exactly the direction exposed by T3k.

It did not prove vanishing of the membrane selector, but it did construct the
correct nontrivial checked-local bridge object.

For equal-trace checked-local pairs `(c, c_ref)` whose local shadows are defined
in a common corrected chart, write their local coefficient vectors as

`(a,b,s)` and `(a_ref,b_ref,s_ref)`.

Because the projected local coefficients are exactly the selected-trace
coordinates, equal selected trace implies

`a = a_ref`, `b = b_ref`.

So the pairwise coefficient difference is automatically

`(0,0,s-s_ref) in span(e_mem)`.

The key new point is that this pairwise membrane difference is invariant under
every quotient-preserving chart change: the affine section shift is the same for
both equal-trace representatives and cancels in the difference.

Therefore there is now a genuine theorem-facing basepoint-relative checked-local
representative-difference object

`Delta_rep,chk,n(q; c, c_ref) in span(e_mem)`,

equivalently a unique scalar membrane selector

`sigma_chk,n(q; c, c_ref)`

such that

`Delta_rep,chk,n(q; c, c_ref) = sigma_chk,n(q; c, c_ref) e_mem`.

On residual-generated pairs this becomes the basepoint-relative selector

`sigma_chk,n(q; c_sel)(z)`.

So the status after T3l is Outcome A:
the correct nontrivial checked-local bridge object is now constructed at the
structural level. What remains open is whether this selector vanishes on the
exact admissible residual-generated pair domain.

### 12.33. T3m implementation stage: the membrane selector closes as the exact surviving cocycle, but vanishing is still obstructed

The next theorem-facing pass pushed that remaining selector question as far as
the current checked-local boundary honestly allows.

For a fixed repo-selected basepoint `c_sel`, the exact residual-generated pair
domain is now recorded as

`D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
(c_sel + z, c_sel) in Pair_chk,n(q) }`.

On this exact domain the basepoint-relative membrane selector

`sigma_chk,n(q; c_sel)(z) := sigma_chk,n(q; c_sel + z, c_sel)`

is no longer just an existence statement. It is now packaged as the exact
chart-invariant membrane cocycle on equal-trace checked-local pairs.

In particular, on the equal-trace checked-local pair domain it satisfies:

- normalization: `sigma_chk(c, c) = 0`;
- antisymmetry: `sigma_chk(c, c_ref) = -sigma_chk(c_ref, c)`;
- cocycle law:
  `sigma_chk(c_1, c_3) = sigma_chk(c_1, c_2) + sigma_chk(c_2, c_3)`.

This is the strongest structural closure now justified for the surviving local
representative-level datum.

But vanishing still does not close.

The reason is now sharper than after T3l:
all currently justified checked-local selected invariants still factor only
through the membrane quotient coordinates `(a, b)`, while `sigma_chk` measures
the representative-level membrane displacement inside one equal-trace quotient
class.

So the status after T3m is Outcome B:
the remaining gap is now an exact selector-level obstruction theorem.

Vanishing of `sigma_chk,n(q; c_sel)(z)` on the full exact domain would require
one additional theorem that the admissible residual-generated checked-local pair
domain meets each equal-trace membrane quotient class only in the repo-selected
representative.

An explicit admissible nonzero example is still not constructed, but an exact
nonvanishing template is now clear:
if an admissible pair exists with common corrected-chart coordinates
`(a, b, s_sel + delta)` and `(a, b, s_sel)` and `delta != 0`, then
`sigma_chk = delta != 0`.

### 12.34. T3n implementation stage: the selector-vanishing question reduces further to patchwise membrane constancy

The next theorem-facing pass pushed the `sigma_chk` question one step further.

It still did not prove vanishing, but it did sharpen exactly what vanishing now
means on the current checked-local boundary.

For fixed repo-selected basepoint `c_sel`, the relevant domain is not the whole
residual space by default, but the exact checked-local definability subdomain

`D_sigma,n(q; c_sel) := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
(c_sel + z, c_sel) in Pair_chk,n(q) }`.

So uniqueness is being tested only where the residual-generated pair is
actually meaningful in a common corrected checked-local chart.

On every such common corrected-chart patch, the membrane selector is now
reduced to a local membrane-coordinate difference:

`sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`.

This means the remaining uniqueness theorem is exactly a patchwise membrane-
constancy theorem.

Vanishing of `sigma_chk` on the exact domain is equivalent to saying that on
every exact admissible residual-generated checked-local pair patch the local
membrane coordinate is constant, or equivalently that the domain meets each
equal-trace membrane quotient class only in the repo-selected representative.

So the status after T3n is Outcome B:
the remaining selector problem is now reduced to an exact patchwise constancy /
uniqueness-in-class obstruction theorem.

Current theorem-facing constraints still determine only the quotient coordinates
`(a, b)`, not the membrane coordinate itself, so they still do not force that
constancy. An explicit admissible nonzero example is still not constructed, but
the nonvanishing template is now sharper: any patch point with
`s_U(z) != s_U(0)` would already produce `sigma_chk != 0`.

### 12.35. T3o implementation stage: overlap compatibility drops out, so only patchwise constancy remains

The next theorem-facing pass asked whether there was still a separate gluing or
overlap obstruction hidden behind the patchwise membrane-coordinate picture.

The answer is now sharper: no.

On each exact admissible residual-generated checked-local patch
`D_sigma^U,n(q; c_sel)`, the selector still has the local-coboundary form

`sigma_chk,n(q; c_sel)(z) = s_U(z) - s_U(0)`.

But if two quotient-preserving corrected charts overlap on the same fixed
equal-trace class, then their membrane coordinates differ only by a constant
shift depending on the fixed selected-trace coordinates `(a_sel, b_sel)` of
that class.

So patchwise constancy is automatically preserved across overlaps.

This means the remaining selector theorem is not blocked by chart gluing.
Global vanishing of `sigma_chk` is equivalent to constancy of `s_U` on any exact
admissible residual-generated checked-local patch cover.

So the status after T3o is Outcome B:
overlap compatibility is now closed as automatic, but patchwise constancy
itself is still not forced by the current theorem-facing constraints.

Current admissibility and candidate structure still determine only the quotient
coordinates `(a, b)`, not the membrane coordinate profile on a patch. So the
single remaining bottleneck is now exactly patchwise constancy itself, not
patch-to-patch compatibility.

### 12.36. T3p implementation stage: the remaining freedom is now isolated as singletonity vs nonsingletonity inside the fixed membrane fiber

The next theorem-facing pass pushed the `T3o` patchwise-constancy picture one
step further.

For every exact admissible residual-generated checked-local patch
`D_sigma^U,n(q; c_sel)`, we now package the exact checked-local patch image

`Im_chk,U,n(q; c_sel) := { chi_chk,U,n(q)(c_sel + z) : z in D_sigma^U,n(q; c_sel) }`.

Because the selected trace is fixed on the whole patch, this image always lies
inside the one-dimensional membrane fiber

`{ (a_sel, b_sel, s)^T : s in R }`.

Equivalently the whole patch is encoded by the membrane-fiber image

`S_U,n(q; c_sel) := { s_U(z) : z in D_sigma^U,n(q; c_sel) }`.

So the remaining constancy problem can now be read exactly as a singleton
question:
vanishing of `sigma_chk`, constancy of `s_U`, singletonity of `S_U`, and
singletonity of `Im_chk,U` are all equivalent.

This is a real sharpening over `T3o`.
`T3o` removed overlap/gluing as an independent obstruction.
`T3p` identifies the exact surviving local freedom on one patch: not general
quotient data, but only the possibility that the exact checked-local patch
image is a nontrivial subset of the fixed membrane fiber above `(a_sel, b_sel)`.

So the status after `T3p` is still Outcome B:
current theorem-facing constraints force only fiber containment, not fiber
singletonity.
An explicit admissible nonsingleton patch is still not constructed, but the
remaining gap is now isolated more sharply than before.


### 12.37. T3q implementation stage: the singletonity question is now isolated as one missing representative law on the exact patch domain

The next theorem-facing pass pushed the T3p singletonity picture one more
step.

It still did not prove singletonity. But it did sharpen exactly why the
current checked-local boundary still cannot force it.

On every exact admissible residual-generated checked-local patch
D_sigma^U,n(q; c_sel), singletonity of the patch image
Im_chk,U,n(q; c_sel) is now repackaged as one patchwise representative law:
all points of that exact patch should determine the same checked-local
representative inside the fixed membrane fiber above (a_sel, b_sel).

Equivalently, on one exact patch the following are all the same statement:
vanishing of sigma_chk, constancy of s_U, singletonity of S_U, and this
patchwise representative law.

The real sharpening over T3p is the obstruction side.
The current theorem-facing checked-local package is still quotient-final on the
checked boundary:
the canonical J_0 trace, the checked local residual, and the next checked
compatibility layer all see only the quotient coordinates (a, b) or are blind
along the membrane line, while the strongest selector candidates checked so far
remain chart-dependent, metric-dependent, or extrinsic.

So the status after T3q is still Outcome B:
singletonity is not closed, but the remaining gap is no longer just "is the
fiber image a singleton?" It is now one exact missing representative-sensitive
law on the exact admissible patch domain.

Any admissible patch with two realized values s_1 != s_2 in the same fixed
fiber would already give a nonzero pairwise selector and hence a genuine
non-singleton obstruction. Such an explicit admissible realization is still
open.

### 12.38. T3r implementation stage: the patchwise representative law reduces further to one pointwise basepoint-relative membrane deviation

The next theorem-facing pass did not prove the patchwise representative law
`Rep_U`.

But it did sharpen that law one more level on the exact admissible patch
domain.

For a fixed repo-selected basepoint `c_sel` and an exact admissible
residual-generated checked-local patch `D_sigma^U,n(q; c_sel)`, the pairwise
law

`chi_chk,U,n(q)(c_sel + z_1) = chi_chk,U,n(q)(c_sel + z_2)`

for all patch points is now reduced exactly to the pointwise basepoint law

`chi_chk,U,n(q)(c_sel + z) = chi_chk,U,n(q)(c_sel)`

for every `z` on that patch.

The key reason is that on every exact patch the checked-local image already
lives in the fixed membrane fiber above the same quotient point `(a_sel,b_sel)`.
So the whole remaining representative difference is now the one-point
basepoint-relative membrane deviation

`Delta_rep,U^pt,n(q; c_sel)(z)
 := chi_chk,U,n(q)(c_sel + z) - chi_chk,U,n(q)(c_sel)
  = sigma_chk,n(q; c_sel)(z) e_mem.`

Therefore the status after `T3r` is still Outcome B, but sharper than after
`T3q`.

The current quotient-final theorem-facing package still forces only

`Delta_rep,U^pt(z) in span(e_mem),`

not

`Delta_rep,U^pt(z) = 0.`

So failure of the full patchwise representative law is now exactly equivalent
to existence of one exact patch point `z_*` with

`sigma_chk,n(q; c_sel)(z_*) != 0,`

equivalently one realized membrane coordinate above `(a_sel,b_sel)` different
from the repo-selected one.

This is the sharpest current reading of the remaining gap below full `T3`:
not another quotient-final theorem, not a new numerical campaign, and not a
return to the frozen local branch, but one pointwise vanishing theorem for the
basepoint-relative membrane deviation on the full exact admissible patch cover.


### 12.39. T3s implementation stage: the patchwise pointwise membrane deviation descends to a chart-invariant exact global defect map

The next theorem-facing pass did not prove pointwise vanishing of the
basepoint-relative membrane deviation.

But it did remove one more layer of patch dependence from the remaining gap.

After `T3r`, the open object was the patchwise pointwise difference
`Delta_rep,U^pt,n(q; c_sel)(z)` on an exact admissible checked-local patch.
`T3s` shows that this object is actually chart-invariant on overlaps, because
quotient-preserving chart changes fix the membrane basis vector `e_mem` and the
pointwise difference already lies in `span(e_mem)`.

So the remaining theorem-facing object can now be written globally on the full
exact pair-definability domain as

`Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem),`

with

`Delta_rep^pt,n(q; c_sel)(z) = sigma_chk,n(q; c_sel)(z) e_mem.`

Therefore the status after `T3s` is still Outcome B, but sharper than after
`T3r`.

The current quotient-final theorem-facing package still forces only that the
exact pointwise defect lies in the membrane line and vanishes at the basepoint
`z = 0`; it still does not force vanishing at an arbitrary exact admissible
point.

So the remaining obstruction is now the exact nonzero set

`N_sigma,n(q; c_sel) := { z in D_sigma,n(q; c_sel) : sigma_chk,n(q; c_sel)(z) != 0 }.`

If that set is empty, the pointwise law closes globally and the remaining
membrane obstruction below the reverse-inclusion / zero-excess bridge
disappears on the current boundary. If it is nonempty, one point already gives
a genuine representative-sensitive obstruction. An explicit admissible nonzero
point is still open.

### 12.40. T3t implementation stage: the global nonzero defect-set question sharpens further to scalar defect-image collapse on the exact domain

The next theorem-facing pass did not prove emptiness of the exact global
nonzero defect set

`N_sigma,n(q; c_sel) := { z in D_sigma,n(q; c_sel) : sigma_chk,n(q; c_sel)(z) != 0 }`.

But it did sharpen the obstruction one more level.

After `T3s`, the remaining object was the chart-invariant global pointwise
defect map `Delta_rep^pt,n(q; c_sel) : D_sigma,n(q; c_sel) -> span(e_mem)` and
its nonzero set `N_sigma`. `T3t` observes that this entire obstruction is
already scalar: the exact surviving data are just the realized values of the
membrane coefficient

`Sigma_sigma,n(q; c_sel) := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }.`

So the question `N_sigma = emptyset` is now exactly equivalent to the scalar
image-collapse statement `Sigma_sigma,n(q; c_sel) = {0}`.

Therefore the status after `T3t` is still Outcome B, but sharper than after
`T3s`.

The current quotient-final theorem-facing package still forces only that the
basepoint contributes the zero scalar value and that all exact pointwise defects
lie along `e_mem`; it still does not force collapse of the whole scalar defect
image to `{0}`.

So the remaining obstruction is now the possibility of one nonzero exact scalar
defect value `delta_* in Sigma_sigma,n(q; c_sel)`, equivalently one exact point
`z_* in D_sigma,n(q; c_sel)` with

`Delta_rep^pt,n(q; c_sel)(z_*) = delta_* e_mem`, `delta_* != 0`.

If the scalar image collapses to `{0}`, then the full defect set is empty and
the remaining membrane obstruction below the reverse-inclusion / zero-excess
bridge disappears on the current boundary. An explicit admissible nonzero point
is still open.

### 12.41. T3u implementation stage: scalar-image collapse sharpens further to vanishing of the exact pairwise scalar-difference image

The next theorem-facing pass did not prove scalar-image collapse

`Sigma_sigma,n(q; c_sel) = {0}`

on the full exact admissible residual-generated domain.

But it did sharpen the obstruction one more level.

After `T3t`, the remaining object was the scalar image

`Sigma_sigma,n(q; c_sel) := { sigma_chk,n(q; c_sel)(z) : z in D_sigma,n(q; c_sel) }`.

`T3u` observes that the exact surviving theorem-facing content is already
pairwise-difference content: every surviving representative-sensitive pairwise
difference is controlled by scalar differences

`Delta_rep,chk(c_sel + z_1, c_sel + z_2)
 = (sigma_chk(z_1) - sigma_chk(z_2)) e_mem`.

So the scalar-image collapse question is now exactly equivalent to vanishing of
the exact pairwise scalar-difference image

`Omega_sigma,n(q; c_sel)
 := { sigma_chk(z_1) - sigma_chk(z_2) :
      (c_sel + z_1, c_sel + z_2) in Pair_chk,n(q) }`.

Because every exact admissible point already pairs with the repo-selected
basepoint and `sigma_chk(0)=0`, one has

`Sigma_sigma,n(q; c_sel) = {0}` iff `Omega_sigma,n(q; c_sel) = {0}`.

Therefore the status after `T3u` is still Outcome B, but sharper than after
`T3t`.

The current quotient-final theorem-facing package still forces only the scalar
cocycle package: basepoint normalization, antisymmetry of exact scalar
differences, and their additivity where the exact admissible pairs compose. It
still does not force all exact scalar differences to vanish.

So the remaining obstruction is now the possibility of one nonzero exact scalar
difference `delta_* in Omega_sigma,n(q; c_sel)`, equivalently one exact point
`z_* in D_sigma,n(q; c_sel)` with

`sigma_chk,n(q; c_sel)(z_*) = delta_* != 0`.

If `Omega_sigma` vanishes, then `Sigma_sigma` collapses to `{0}`, the full
defect set is empty, and the remaining membrane obstruction below the reverse-
inclusion / zero-excess bridge disappears on the current boundary. An explicit
admissible nonzero-scalar realization is still open.
### 12.42. T3v implementation stage: pairwise scalar-difference collapse is still open, but the exact missing ingredient is now one representative-sensitive rigidity law on the admissible pair domain

The next theorem-facing pass did not prove pairwise scalar-difference collapse

`Omega_sigma,n(q; c_sel) = {0}`

on the full exact admissible pair domain.

But it did sharpen the obstruction one more level.

After `T3u`, the remaining object was the exact pairwise scalar-difference
image

`Omega_sigma,n(q; c_sel)
 := { sigma_chk(z_1) - sigma_chk(z_2) :
      (c_sel + z_1, c_sel + z_2) in Pair_chk,n(q) }`.

`T3v` makes the exact pair domain itself explicit:

`Pair_sigma,n(q; c_sel)
 := { (z_1, z_2) in D_sigma,n(q; c_sel)^2 :
      (c_sel + z_1, c_sel + z_2) in Pair_chk,n(q) }`.

This yields the sharper exact relation

`Sigma_sigma,n(q; c_sel) subseteq Omega_sigma,n(q; c_sel)
 subseteq Sigma_sigma,n(q; c_sel) - Sigma_sigma,n(q; c_sel)`,

because every exact admissible point already pairs with the repo-selected
basepoint, while not every pair of exact admissible points is silently assumed
to be admissible.

Therefore the status after `T3v` is still Outcome B, but sharper than after
`T3u`.

The current theorem-facing admissibility / candidate package still forces only
quotient-final data: the fixed quotient coordinates `(a_sel, b_sel)` and the
scalar cocycle package for exact pairwise differences. It still does not force
equality of membrane coordinates inside the fixed quotient fiber.

So the remaining obstruction is now one exact representative-sensitive
rigidity question:

`can there exist exact admissible pair data (z_1, z_2) in Pair_sigma,n(q; c_sel)`

with checked-local representatives

`chi_chk,chart(c_sel + z_i) = (a_sel, b_sel, s_i)^T`

and

`s_1 != s_2`?

If no such pair exists, then `Omega_sigma = {0}`, hence `Sigma_sigma = {0}`,
the exact defect set is empty, and the remaining membrane obstruction below the
reverse-inclusion / zero-excess bridge disappears on the current boundary.
If such a pair exists, then it gives a genuine exact nonzero pairwise scalar-
difference obstruction.

### 12.43. Admissible-lift branch: the current selected full-center lift carries no nonzero same-trace admissible membrane lift

After the `T3 ... T3v` chain saturated under the current quotient-final ideas,
the next concrete question became the admissible-lift branch:
can the local surviving membrane mode be realized by an exact admissible global
same-trace lift?

A new exact obstruction is now available on the global selected side.

Let

`X_sel,n(q) := im(P_sel,n(q))`,
`C_center,n(q) P_sel,n(q) = I_4`,
`A_ls,n(q) = im(P_sel,n(q) D_amp)`.

Then `C_center|_(X_sel,n(q))` is bijective with inverse `P_sel,n(q)`.
So if `c_sel in A_ls,n(q)` and

`z in A_adm^th,n(q) intersect ker(C_center,n(q))`

also satisfies `c_sel + z in X_sel,n(q)`, then

`C_center(c_sel + z) = C_center(c_sel)`

forces `c_sel + z = c_sel`, hence `z = 0`.

Therefore the selected-architecture lift class

`Lift_mem^sel,n(q; c_sel)
 := { z in A_adm^th,n(q) intersect ker(C_center,n(q)) :
      c_sel + z in X_sel,n(q),
      (c_sel + z, c_sel) in Pair_chk,n(q) }`

is exactly trivial.

Equivalently,

`A_sel^{th,cand},n(q) intersect X_sel,n(q) = A_ls,n(q)`.

So the local membrane mode cannot be lifted by moving inside the already closed
KKT-selected global architecture. Any future admissible-lift construction, if
it exists at all, must be genuinely extrinsic to `X_sel`, hence outside the
current repo-selected family `A_ls`.

This is not full impossibility of admissible lifts in all of `A_adm^th`, but it
is a real exact restriction sharper than the previous `Omega_sigma`-only
packaging. The next unresolved point is whether candidate-class points outside
`X_sel` can remain same-trace admissible and checked-local pair-definable while
still carrying the membrane direction.
### 12.44. Extrinsic admissible-lift branch: after the `X_sel` obstruction, outside-`X_sel` is automatic and the real bottleneck sits on the residual fiber itself

The last decisive obstruction already killed all same-trace admissible lifts
inside the current global selected full-center lift `X_sel = im(P_sel)`.

A further exact simplification is now available.

Because `C_center P_sel = I_4`, one has

`X_sel,n(q) intersect ker(C_center,n(q)) = {0}`.

So for every repo-selected basepoint `c_sel in A_ls,n(q) subset X_sel,n(q)` and
for every nonzero same-trace residual direction

`0 != z in A_adm^th,n(q) intersect ker(C_center,n(q))`,

it follows automatically that

`c_sel + z notin X_sel,n(q)`.

Therefore the extrinsic admissible-lift question no longer has an independent
"outside `X_sel`" part. That condition is automatic for every nonzero same-
trace residual.

What remains is narrower and sharper:
one needs an exact theorem on the residual fiber

`A_adm^th,n(q) intersect ker(C_center,n(q))`

that decides which nonzero directions are checked-local pair-definable with the
selected basepoint and whether they produce nonzero representative-sensitive
membrane deviation.

So the current theorem path is not blocked any more by `X_sel`. It is blocked by
absence of a global-to-local admissibility / pair-definability / membrane-
visibility theorem on the 44-dimensional residual fiber itself.
### 12.45. Residual-fiber branch: any membrane-visible candidate residual must already satisfy the exact low-order membrane-nullmode equations

The residual-fiber question now has one more exact restriction.

Let

`R_res,n(q) := A_adm^th,n(q) intersect ker(C_center,n(q))`.

Under the same checked local nonresonance regime already used in pilot 23, if

`0 != z in R_res,n(q)`

is checked-local pair-definable with the selected basepoint and has nonzero
representative-sensitive membrane deviation, then its coefficient-faithful
augmented checked-local residual jet must lie in the one-dimensional line

`span(g_mem^aug,n(q))`,
`g_mem^aug,n(q) = [0,0,0,0,alpha,0,0,0,beta,1]`.

So its first checked nontrivial coefficients are not arbitrary. They must obey

`U1 = alpha T1`, `V1 = beta T1`, `N1 = P1 = Y1 = 0`, with `T1 != 0`,

and after that membrane mode is substituted, the checked next layer closes
uniquely to zero.

This is a real residual-fiber obstruction: the search is no longer over all of
`R_res`, but only over residual directions whose extracted low-order local jet
matches the exact membrane-nullmode equations.

So the remaining missing input is now sharper than just "something on the
residual fiber": one needs a global checked-local coefficient-extraction theorem
on `R_res` deciding whether a given residual direction realizes that exact
augmented membrane-nullmode jet.
### 12.46. Residual-fiber branch: the current weighted ansatz already gives an explicit global same-trace template realizing the membrane-nullmode jet

A genuinely new point is now closed beyond the already known local
`span(g_mem^aug)` restriction. On the current clean weighted-ansatz repository
boundary, the membrane-nullmode low-order jet is not only necessary; it is also
explicitly realizable by a global same-trace residual coefficient family.

With `L = 1 - x0` and `s_mem != 0`, taking only the six coefficients
`u_s,k=1,2`, `v,k=1,2`, and `T_s,k=1,2` nonzero, with values
`(-L alpha s_mem, -(L^2/x0) alpha s_mem)`,
`(-L beta s_mem,  -(L^2/x0) beta s_mem)`, and
`(-L s_mem,       -(L^2/x0) s_mem)`, gives a global trial object in
`ker(C_center)` whose exact center expansion is
`u_s = alpha s_mem x^(n+1) + O(x^(n+2))`,
`v   = beta  s_mem x^(n+1) + O(x^(n+2))`,
`T_s =       s_mem x^n     + O(x^(n+1))`,
with all quotient/flexural low-order coefficients zero.

So the weighted-ansatz / coefficient architecture itself does not obstruct
realization of the membrane-nullmode jet. This pushes the branch toward the
counterexample side on the current repo boundary. The remaining open issue is
now sharper: whether the full theorem-facing admissible / pair-definable class
upgrades this explicit weighted-ansatz template into a true exact admissible
membrane-visible lift, or whether some additional admissibility theorem blocks
that upgrade.
### 12.47. Explicit membrane template: the current stop is now exactly the theorem-facing admissibility / pair-check upgrade

After constructing the explicit weighted-ansatz membrane template, the branch is
no longer blocked by low-order realizability of the membrane-nullmode jet.

The next honest check was whether this explicit object already gives a genuine
nonzero admissible lift. The conservative answer on the present exact repository
boundary is no: the extension fails earlier, at the theorem-facing upgrade from
an explicit weighted trial coefficient vector to an element of `A_adm^th` whose
pair with `c_sel` lies in `Pair_chk`.

This is sharper than the earlier logs. If that checked-local shadow upgrade were
available, the final membrane deviation would not be the issue: in the visible
corrected chart the membrane direction is the `U1` direction, and the template
already has `U1 = alpha s_mem != 0` on the physical clean regime. So the exact
remaining obstacle is not jet realizability and not final membrane visibility;
it is the admissibility / checked-local-shadow upgrade itself.