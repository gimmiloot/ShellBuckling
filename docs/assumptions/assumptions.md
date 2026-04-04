# Assumptions used in the project

## Статус документа

В этом файле перечислены именно **введённые предположения**, а не все результаты подряд.

Для каждого предположения указано:
- его формулировка;
- проверялось ли оно;
- если да, то как именно;
- какой у него текущий статус:
  - **подтверждено**;
  - **частично подтверждено**;
  - **не подтверждено**;
  - **снято / отвергнуто**.

---

## LC. Локальная реализуемость / punctured continuation для clean full simple-support `J_0` ветки

**Формулировка.** Для фиксированных `(n,q)` каждый
`c in A_full^th,n(q)` допускает `\delta > 0` и punctured near-center clean
mixed continuation на `(0,\delta)` в текущих mixed variables, удовлетворяющее
текущим local clean mixed equations и intended near-center scaling orders.

**Проверялось ли:** нет, theorem-facingly на этой ветке пока не доказано.

**Как используется:** как явное рабочее физическое предположение away from the
center, чтобы не переформулировать бесконечно один и тот же ambient-to-local
closure barrier. Все последующие theorem-facing local steps, которые используют
punctured local continuation, должны читаться **условно под Assumption LC**,
если независимое closure-доказательство не получено.

**Текущий статус:** **не подтверждено**.

---

## LC-HM. Взвешенное harmonic-mean admissibility fallback для clean full simple-support `J_0` ветки

**Формулировка.** Условно под Assumption LC, если theorem-facing one-sided
control on
`S = -(1-c_0) + (1-\nu^2)T_{s0}c_0`
через scalar Riccati comparison for
`u = \lambda_{\theta 0}^{-1}`, `\lambda_{\theta 0} = r_0/x`,
не получен из текущего clean background ODE/BC package, то на
LC-conditional line принимается минимальное fallback assumption
`\int_{x_0}^1 \eta(x)/(x\lambda_{\theta 0}(x))\, dx
 \le \int_{x_0}^1 \eta(x)/x\, dx`,
эквивалентно
`D(1) = \int_{x_0}^1 [\eta(x)/x](1-\lambda_{\theta 0}(x)^{-1})\, dx \ge 0`.

**Проверялось ли:** нет, theorem-facingly из текущего clean background
package пока не выведено.

**Как используется:** как минимальное weak weighted circumferential-stretch
admissibility condition на активной clean LC-conditional line; оно строго
слабее pointwise `\lambda_{\theta 0}\ge 1` и слабее глобальных sign
assumptions на `\varphi_0`, `c_0`, `e_{\theta 0}`. Более сильные
pointwise/geometric assumptions не должны вводиться по умолчанию, пока не
станет ясно, что они действительно необходимы для Riccati comparison.

**Текущий статус:** **не подтверждено**.

---

## A1. Простая замена background внутри старой reduced/full архитектуры может исправить критерий

**Формулировка.** Было предположение, что достаточно заменить докритический фон, не меняя принципиально сам старый linearized class.

**Проверялось ли:** да.

**Как проверялось:** на ветках `F_min_reduced`, `F_min_full_v2`, `F_min_full_v3_chernykh`.

**Результат проверки:** качественного сдвига критерия не произошло.

**Текущий статус:** **снято / отвергнуто**.

---

## A2. Проблема сидит в одной closure-формуле или только в правом крае

**Формулировка.** Предполагалось, что достаточно починить одну closure-связь или одну граничную строку.

**Проверялось ли:** да.

**Как проверялось:** серией частичных ремонтов старой архитектуры и сравнением поведения критерия до и после локальных исправлений.

**Результат проверки:** проблема оказалась структурной и шире одной формулы.

**Текущий статус:** **снято / отвергнуто**.

---

## A3. Corrected kinematics и corrected circumferential bending block являются базовыми и их нужно сохранять

**Формулировка.** После перехода к новой mixed-weak ветке предполагалось, что corrected kinematics и corrected circumferential bending block не должны больше пересматриваться как главный источник ошибки.

**Проверялось ли:** да.

**Как проверялось:** все последующие mixed-weak derivations и testbench-ветки строились именно на этих блоках; они не давали внутренних противоречий в тех проверках, которые были выполнены.

**Результат проверки:** эти блоки работают как устойчивая база новой ветки.

**Текущий статус:** **частично подтверждено**.

**Почему не «полностью подтверждено»:** не выполнена ещё отдельная замкнутая перепроверка всей общей теории от начала до конца в одном тексте.

---

## A4. Новый operator class должен содержать независимые окружные каналы `(v,S)` и `(psi,H,chi)`

**Формулировка.** Предполагалось, что без независимых окружных каналов новый критерий не получится.

**Проверялось ли:** да.

**Как проверялось:**
- через формальный вывод нового класса;
- через проверку conjugate pairs на краю;
- через построение surrogate mixed-weak solver/testbench.

**Результат проверки:** новый класс действительно использует эти каналы содержательно; без них постановка схлопывается назад к старой closure-логике.

**Текущий статус:** **частично подтверждено**.

---

## A5. Prestress/load part не замыкается в scalar potential `G(U)`, а должен задаваться как bilinear weak-form `G_ps(U,Uhat)`

**Формулировка.** Предполагалось, что forcing-блок в новой постановке intrinsically несимметричен и не должен насильственно упаковываться в один потенциал.

**Проверялось ли:** да.

**Как проверялось:** через вывод corrected meridional/normal forcing и проверку функционального маршрута на краю и в bulk.

**Результат проверки:** bilinear weak-form оказалась рабочей, scalar-potential route — нет.

**Текущий статус:** **частично подтверждено**.

---

## A6. У нового mixed weak class снова двумерное central regular family

**Формулировка.** Предполагалось, что после расширения operator class размер physical regular family у центра остаётся равным двум.

**Проверялось ли:** да.

**Как проверялось:** principal-part анализом и построением двух central regular modes в `mixed_weak_boundary_matrix_test_v2`.

**Результат проверки:** в рабочей ветке это именно так и использовалось.

**Текущий статус:** **частично подтверждено**.

---

## A7. `sigma_min(B_mix(q)) = 0` — правильный рабочий mixed-weak criterion

**Формулировка.** Предполагалось, что новая boundary matrix `B_mix` должна играть роль главного spectral criterion.

**Проверялось ли:** да.

**Как проверялось:** на testbench-ветках `mixed_weak_boundary_matrix_test.py` и `mixed_weak_boundary_matrix_test_v2.py`.

**Результат проверки:** критерий оказался вычислимым и содержательным как рабочий exploratory criterion.

**Текущий статус:** **частично подтверждено**.

**Почему не «полностью подтверждено»:** ещё нет финальной строгой BVP-реализации и строгого доказательства, что именно этот критерий является окончательным для полной постановки.

---

## A8. Текущий mixed-weak минимум при `n=13`, `q≈3.79..3.80 MPa` отражает реальный физический `q_cr` для simple support

**Формулировка.** На одном этапе предполагалось, что найденный mixed-weak кандидат уже можно интерпретировать как окончательную критическую нагрузку для simple support.

**Проверялось ли:** да.

**Как проверялось:** через анализ архитектуры solver’а и затем через разбор того, как именно в задачу был введён simple support.

**Результат проверки:** выяснилось, что background и критическое возмущение были ещё не полностью согласованы по типу закрепления.

**Текущий статус:** **не подтверждено**.

**Комментарий:** значение `3.79..3.80 MPa` сохраняется как **exploratory mixed-weak candidate**, но не как окончательный результат полной задачи.

---

## A9. Для полной simple-support задачи достаточно заменить только правую boundary matrix критического критерия

**Формулировка.** Неявно предполагалось, что фон можно оставить старым, а simple support вводить только в критической задаче.

**Проверялось ли:** да.

**Как проверялось:** именно так и были получены ранние simple-support mixed-weak результаты.

**Результат проверки:** для полной физически согласованной задачи этого недостаточно.

**Текущий статус:** **снято / отвергнуто**.

---

## A10. По названиям осесимметрические BC simple support имеют вид `T_s(1)=0`, `M_s(1)=0`, `u_z(1)=0`

**Формулировка.** Предполагалось, что для непологой осесимметрической задачи полный simple support должен задаваться именно так.

**Проверялось ли:** да, но не полностью.

**Как проверялось:**
- по физическому смыслу условий;
- по сопоставлению с используемыми переменными осесимметрической постановки;
- по обсуждению с FEM-условиями на уровне названий.

**Результат проверки:** по названиям и смыслу это выглядит корректным рабочим кандидатом.

**Текущий статус:** **частично подтверждено**.

**Почему не «полностью подтверждено»:** ещё не доказано, что в текущих смешанных переменных это полностью эквивалентно FEM-постановке без скрытых различий.

---

## A11. Ранний continuation ceiling в районе `q≈4.344..4.36 MPa` является физической точкой потери устойчивости

**Формулировка.** После первых неудачных запусков simple-support background solver’а можно было бы интерпретировать старый барьер около `4.344 MPa` или более ранние срывы около `4.36 MPa` как физическую точку потери устойчивости.

**Проверялось ли:** да.

**Как проверялось:**
- сравнением с FEM-оценкой критической нагрузки порядка `10 MPa`;
- анализом того, что continuation ceiling заметно сдвигается без изменения equations и без изменения simple-support BC set: old path `4.3434 / 4.3440 MPa`, pilot 20 `4.3520 MPa`, audited pilot 21 `4.3800 MPa`;
- новым checkpointed fast run, который локально дошел до `6.0000 MPa` без bounded failure в сохраненной ladder;
- более строгим milestone-audit на `4.4000 MPa`, который в двух независимых pointwise confirm-проверках остается near-reproducible на том же accepted seed, не показывает branch-jump suspicion и не дает bounded failure до `4.4100 MPa`;
- sparse confirm на `5.0000`, `5.5000` и `6.0000 MPa`, который не показывает bounded first failure до `6.0040 MPa`, сохраняет тот же accepted seed и отсутствие branch-jump suspicion, но выше `5.0 MPa` выходит за текущий near-reproducible threshold из-за малого гладкого repeat drift;
- targeted diagnostic того, что strict-false сейчас в первую очередь задается текущей confirm-policy / threshold logic, а не явным branch-loss signal;
- сопоставлением с литературой по hinged support.

**Результат проверки:** такая интерпретация не выдерживает проверки.

**Текущий статус:** **снято / отвергнуто**.

## A12. Главная проблема полной simple-support задачи — в осесимметрическом background solver’е

**Формулировка.** Сейчас рабочая гипотеза состоит в том, что главная открытая проблема сидит именно в осесимметрическом simple-support background, а не в уже найденной mixed-weak критической части.

**Проверялось ли:** частично.

**Как проверялось:**
- через анализ различия между old background и full simple support;
- через прямые попытки решить осесимметрический BVP с `M_s(1)=0`;
- через сравнение с FEM и литературой.

**Результат проверки:** именно этот узел сейчас выглядит основным препятствием.

**Текущий статус:** **частично подтверждено**.

---

## A13. Для hinged support при больших нагрузках уравнения пологих оболочек могут плохо описывать докритическое состояние

**Формулировка.** Предполагалось, что shallow-shell background может становиться недостаточно точным именно в hinged/simple-support задачах при больших нагрузках.

**Проверялось ли:** да, косвенно.

**Как проверялось:**
- по литературным указаниям Bauer–Semenov–Voronkova и смежных работ;
- по сравнению аналитического solver’а с FEM;
- по наблюдаемым трудностям при simple support.

**Результат проверки:** это согласуется и с литературой, и с текущими численными наблюдениями.

**Текущий статус:** **частично подтверждено**.

---

## A14. Следующий правильный шаг — сначала стабилизировать осесимметрический фон, а потом возвращаться к `q_cr`

**Формулировка.** Предполагается, что искать окончательную критическую нагрузку для полной simple-support задачи раньше, чем найден устойчивый осесимметрический фон, методически неправильно.

**Проверялось ли:** нет в виде численного эксперимента, это организационный вывод.

**Как проверялось:** логическим анализом зависимости критической задачи от background и того, что уже не удалось получить напрямую.

**Текущий статус:** **не подтверждено как математический факт**, но принято как **рабочая стратегия проекта**.

---

## A15. Для продвижения separate 6-state simple-support ветви к нагрузкам порядка `10 MPa` правильнее разделять быстрый checkpointed continuation и редкий confirm/audit

**Формулировка.** Предполагается, что повторять тяжелый pilot-style audit при каждом новом подъеме по нагрузке методически и вычислительно невыгодно; вместо этого лучше использовать один быстрый resumable runner на `u_z`-scaled + auxiliary arc-like workflow и отдельный confirm runner только для milestone-точек.

**Проверялось ли:** частично.

**Как проверялось:**
- прямой реализацией нового checkpoint/resume слоя поверх pilot 21;
- from-scratch fast run до `4.3900 MPa`;
- resume-run продолжением через `4.4200`, `4.4400`, `4.4600`, `4.4800` и `4.5000 MPa` без повторного прогрева всей ветви снизу;
- двумя дополнительными resume-run, которые довели ветвь от `4.5000` до `6.0000 MPa` примерно за `35 s` суммарно без bounded failure;
- dedicated `4.4000 MPa` milestone-audit и sparse confirm run на сохраненных checkpoint’ах для `5.0000`, `5.5000` и `6.0000 MPa`;
- targeted comparison confirm-метрик на `4.4000`, `4.4600`, `4.5000`, `5.0000`, `5.5000` и `6.0000 MPa`.

**Результат проверки:** как инженерная workflow-стратегия это уже выглядит существенно дешевле и лучше масштабируется, но два открытых ограничения остаются явными: текущий strict reproducibility gate, похоже, слишком жесток относительно smooth same-branch drift, а текущий controller cap `MAX_STEP_MPA = 0.0025` уже сам становится следующим runtime bottleneck для дальнейшего ускорения подъема.

**Текущий статус:** **частично подтверждено как operational strategy**, не как theorem-level claim.

---

## A16. Для clean full `simple support / подвижный шарнир` theorem-level target объектом должно быть вырождение reduced tangent operator на admissible center-regular space, а не сразу raw `B_mix`

**Формулировка.** Предполагается, что для clean standalone full `simple support / подвижный шарнир` задачи правильный theorem-level target должен задаваться не одним только raw boundary-only object `B_mix`, а полным reduced tangent operator `L_red,n(q)`, полученным из stacked full operator `[A_int(q); B_full(q)]` после редукции на admissible center-regular двумерное пространство.

**Проверялось ли:** частично.

**Как проверялось:**
- ручным выводом из live clean architecture (`A_int`, `B_full`, `C_center`, `V_reg`);
- CAS-проверкой block identities и reduction formulas в `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`;
- representative numerical checks на clean competition set `n=4,6,7,8`.

**Результат проверки:** как repository-level structural/formal target этот объект уже можно зафиксировать явно; кроме того, на текущем выбранном reduced family `A_repo = im(V_adm)` теперь уже есть точная конечномерная C3-идентификация
`ker(L_red) <-> A_repo ∩ ker(L_full)`.
При этом всё ещё не доказано, что `A_repo` совпадает с полным admissible clean center-regular tangent space, и не доказана equivalence между `ker(L_red)` и boundary-only reading `sigma_min(B_mix)=0`.

**Текущий статус:** **частично подтверждено как finite-dimensional algebraic reduction на текущем reduced family; full theorem-level closure ещё открыта**.

---

## A17. Для clean full `simple support / подвижный шарнир` текущий repo-selected family `A_repo = im(V_adm)` должен быть lossless, то есть совпадать с full admissible clean center-regular tangent space

**Формулировка.** Предполагается, что current repo-selected reduced family
`A_repo,n(q) = im(V_adm,n(q))` не просто является удобным current construction,
а действительно совпадает с тем full admissible clean center-regular tangent
space, который должен задавать theorem-level criticality.

**Проверялось ли:** частично.

**Как проверялось:**
- ручным разделением theorem-facing full admissible space, weighted trial
  coefficient space `X_trial`, pure center-regular coefficient space
  `W_reg = ker(C_reg)`, и current selected KKT-family;
- CAS / algebra checks для leading center block и двухпараметрической
  parameterization regular leading data;
- live checks для rank / dimension facts и для совпадения `im(V_adm)` с
  current KKT-selected amplitude family на representative clean points;
- отдельным principal-part local derivation helper для leading singular block
  current mixed equations.

**Результат проверки:** текущий repository теперь знает следующее точно:
- leading admissible center data действительно двумерны;
- singular leading block current principal center model тоже использует те же
  free amplitudes `(A_us, A_phi)`;
- `A_repo = im(V_adm)` совпадает с exact current KKT-selected amplitude family
  внутри weighted trial ansatz;
- но fully frozen principal higher-order recurrence даёт более жёсткую
  finite-order картину: generic full leading layer зануляется, next layer
  оставляет только one-parameter membrane mode `T1`, а checked second layer
  снова uniquely zero;
- дополнительная C3c-проверка показала, что и restored first-finite center
  coefficients current clean background тоже недостаточны: they start only at
  `O(x^2)` / `O(x^3)` and do not alter the same lowest obstruction layer in
  `R_Ts`, `R_Ms`, and `R_v`, so the richer checked local model still forces
  `P0 = 0` generically on the active clean path;
- поэтому equality между `A_repo` и full theorem-facing clean admissible tangent
  space по-прежнему не доказана. Main missing ingredient now narrowed again:
  нужен local ingredient that can act at the same lowest obstruction orders, or
  же нужен пересмотр exact theorem-facing local comparison object; simply adding
  the first omitted finite center coefficients is already known to be
  insufficient.

**Текущий статус:** **не подтверждено как theorem-level факт; закрыты ansatz-level characterization текущего selected family, singular leading-block matching и finite-order frozen-principal obstruction, но full local/global completeness ещё открыта**.

---

## A18. Для clean full `simple support / подвижный шарнир` correct comparison object для `A_ls` должен включать weak/KKT selection layer, а не совпадать по умолчанию с raw unrestricted local center-regular family

**Формулировка.** Предполагается, что после C3b/C3c вопрос о losslessness нельзя
по умолчанию формулировать как прямое сравнение current KKT-selected family
`A_ls = im(M_amp) = im(V_adm)` со всей unrestricted local center-regular clean
family. Более plausibly correct theorem-facing comparison object должен быть
уже **selected**:
- либо local center-regular family + weak/interior optimality selection,
- либо local germ family глобально weak-selected admissible family.

**Проверялось ли:** частично.

**Как проверялось:**
- structural inspection live clean code path `full_simple_support_critical_search.py`;
- явным выписыванием KKT problem
  `min ||A_int c||^2 + reg ||c||^2` при `C_center c = [a1, a2, 0, 0]`;
- helper-скриптом
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`,
  который проверяет размер amplitude fiber, KKT stationarity / fiber
  orthogonality, и сравнивает full selected map с near-center-only surrogate
  objectives.

**Результат проверки:** current repository теперь знает следующее:
- для фиксированных amplitudes weighted trial ansatz оставляет большой affine
  fiber размерности `44`;
- `A_ls` — это не весь этот fiber и не просто chart для center regularity, а
  его unique `H = A_int^T A_int + reg I`-minimal KKT-selected section;
- simple constraint-only feasible representatives имеют full objective больше на
  many orders of magnitude;
- near-center-only surrogate objectives не reproduces тот же selected map,
  значит адекватный purely local KKT analogue пока не виден.

**Текущий статус:** **частично подтверждено как current structural reading, но не как theorem-level локальная теорема**.


## A19. На текущем clean full `simple support / подвижный шарнир` path лучший точно определённый theorem-facing local selected object задаётся как локальный trace глобальной KKT-selected family, а не как raw `A_reg^loc`

**Формулировка.** После C3e рабочая гипотеза стала строже. Пусть
`A_reg^loc` обозначает raw local center-regular formal family clean mixed
уравнений, а `A_ls = im(M_amp) = im(V_adm)` — текущую глобальную
weighted-trial KKT-selected family live clean code path. Тогда лучший точно
определённый local comparison object, который сейчас реально виден в
репозитории, есть

```text
A_sel,trace^loc := J_0(A_ls),
```

то есть local germ / center trace глобально selected family. Внутренняя purely
local characterization того же объекта внутри `A_reg^loc` через canonical local
weak/KKT-type rule пока не выведена.

**Проверялось ли:** частично.

**Как проверялось:**
- structural inspection live clean KKT assembly в
  `full_simple_support_critical_search.py`;
- helper-скриптом
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`,
  который выписывает selected 4D center-data lift, отделяет fixed-center fiber
  от selected slice и проверяет representative clean points;
- сопоставлением с уже закрытыми local obstruction checks в
  `formal_local_family_check.py`, которые показывают, что raw local object сам
  по себе не может больше считаться default comparison target.

**Результат проверки:**
- current `A_ls` действительно содержит selection layer сверх raw center
  regularity;
- best exact faithful local candidate currently visible is
  `A_sel,trace^loc = J_0(A_ls)`;
- canonical intrinsic local selected family is not yet identified.

**Текущий статус:** **частично подтверждено как theorem-facing formulation, но не закрыто как local theorem**.

## A20. На текущей clean full `simple support / подвижный шарнир` boundary лучший theorem-facing trace map есть finite leading-center jet `J_0 = C_center`, а selected trace object exactly equals `J_0(A_ls) = im(D_amp)`

**Формулировка.** После C3f рабочая формулировка становится точнее. На current
weighted-trial clean path `J_0` не следует по умолчанию понимать как полный
higher-order local germ. Лучший current theorem-facing meaning есть finite
leading-center jet map

```text
J_0(c) := C_center c,
```

который хранит две leading amplitudes и две leading regularity-defect rows.
Тогда для current selected family

```text
A_ls = im(P_sel D_amp)
```

selected trace object exactly reads

```text
J_0(A_ls) = im(D_amp),
```

а restriction `J_0|_{A_ls}` является basis-independent bijection onto this 2D
selected plane, with inverse given by the selected lift `P_sel` on that plane.

**Проверялось ли:** да, на current weighted-ansatz / leading-center-jet level.

**Как проверялось:**
- structural inspection `make_center_constraint_matrix(...)` в
  `full_simple_support_critical_search.py` и `TrialSpace.basis_eval(...)` в
  `solver_patched_core.py`;
- helper-скриптом
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`,
  который проверяет exact active center columns, `C_center P_sel ≈ I_4`,
  `C_center M_amp ≈ D_amp`, reconstruction from trace, and basis-change
  invariance of the selected trace plane;
- symbolic center-block check in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/reduction_check.py`.

**Результат проверки:**
- best current theorem-facing meaning of `J_0` is finite leading-center jet,
  not a full unresolved higher-order germ;
- `J_0(A_ls)` is exactly the selected 2D plane `im(D_amp)` on the current
  weighted-ansatz boundary;
- intrinsic higher-order local selector is still not identified.

**Текущий статус:** **закрыто на current weighted-ansatz / leading-center-jet level, но не как full intrinsic local-germ theorem**.
## Короткая сводка по статусам

### Подтверждено / частично подтверждено
- A3, A4, A5, A6, A7, A10, A12, A13, A15, A16, A18, A19, A20.

### Не подтверждено
- A8, A14, A17.

### Снято / отвергнуто
- A1, A2, A9, A11.

---

## Источники, на которые опирался этот файл

- `docs/journal/project_journal_updated14.md`
- `docs/theory/vyvod_uravneniy_updated17.md`
- `docs/theory/current_simple_support_status.md`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `proof_pilots/pilot_20_method_sweep_for_simple_support_ceiling/pilot_20_method_sweep_for_simple_support_ceiling.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/pilot_21_u_z_scaled_arc_like_continuation.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_continuation_workflow.md`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/fast_progress.json`
- `proof_pilots/pilot_21_u_z_scaled_arc_like_continuation/fast_run/confirm_results.json`
- `holm3.pdf`
- `BauerVoronkovaSemenov-vestnik2022_1.pdf`


## A21. For the current C3g comparison, the continuum/local selected trace must be written in the same `J_0 = C_center` coordinates as the live clean architecture; in those coordinates the singular local selected trace equals `im(D_amp)`

**Statement.** After C3g, the project-level comparison between the selected global
trace and the continuum/local side should not be made on an arbitrary local jet
coordinate choice. The current theorem-facing comparison object is the leading-
center trace written in the same coordinates as the exact live clean trace map

```text
J_0(c) = C_center c,
```

that is,

```text
[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0].
```

In these coordinates the singular local compatibility equations imply

```text
[U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0]
= D_amp [U0, P0],
```

so the current selected leading-center trace plane on the local side is exactly
`im(D_amp)`.

**Checked:** yes, but only at the leading-center-jet level.

**Verification used:**
- symbolic derivation in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- structural inspection of the live clean background definitions in
  `axisymmetric_simple_support_background.py`,
  `full_simple_support_critical_search.py`, and `solver_patched_core.py`;
- representative live clean checks that the truncated background BCs give
  `u_r(x0) = 0` and hence `lambda_theta0(x0) = 1` at the current selected
  `x0`-trace layer.

**Result:**
- the current continuum/local selected leading-center trace agrees exactly with
  `im(D_amp)` when written in the same coordinates as `J_0 = C_center`;
- this is already enough to justify `im(D_amp)` as the next theorem-facing
  comparison object beyond the raw unrestricted local family;
- but it still does **not** identify a full intrinsic higher-order local
  selector.

**Current status:** **closed only at the leading-center-jet level in current `J_0` coordinates**.


## A22. The richer local trace is best treated as a normalization-dependent truncated jet, and the invariant selected object is its 2D lifted family projecting canonically to `im(D_amp)`

**Statement.** After C3h, the project should not ask whether every richer local
trace chart has the same literal zero-defect slice as current `J_0`. The best
current richer local object is the truncated regular-singular jet

```text
Xi_rich^(1,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1],
```

with explicit normalization parameter `eta` in the fourth coordinate. The
canonical relation to the current selected trace is the projection
`Pi_eta_to_J0`, and the invariant selected object is the 2D lifted plane inside
that richer trace whose `J_0` projection equals `im(D_amp)`.

**Checked:** yes, at the trace-reconciliation / truncated-jet level.

**Verification used:**
- symbolic derivation in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- structural reading of the current `J_0 = C_center` coordinates from the live
  clean code;
- representative live clean checks that the special case `eta = 1` carries the
  lifted fourth coefficient `(lambda_c - 1) P0`, so the older richer chart is a
  different normalization rather than a contradiction.

**Result:**
- richer local trace charts are now reconciled with `J_0` by an explicit
  projection formula;
- the selected object that should be preserved at higher order is a lifted 2D
  family, not a coordinate-dependent zero-defect slice in every richer chart;
- a full higher-order selected-family theorem is still open.

**Current status:** **closed only at the trace-reconciliation / truncated-jet level**.


## A23. The first higher-order selected object is a one-parameter membrane thickening over the lifted selected plane

**Statement.** After C3i, the project should not expect the raw lifted 2D plane
`im(D_rich,eta)` to remain exactly preserved at the first checked post-leading
order. The checked recurrence instead preserves a corrected object: a
one-parameter membrane thickening over that lifted selected plane. In the
current richer jet it appears as

```text
Xi_sel,corr^(1,eta)
  = {[U0, P0, 0, (lambda_c - eta) P0, U1, 0, 0, 0]},
```

while a coefficient-faithful version uses an augmented jet with explicit
membrane nullmode `(U1, V1, T1) = T1 * (alpha, beta, 1)`. The canonical
projection of either corrected object to current `J_0` coordinates remains
exactly `im(D_amp)`.

**Checked:** yes, at the first checked post-leading recurrence level.

**Verification used:**
- symbolic derivation in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- symbolic proof that the first checked post-leading recurrence is independent
  of the leading selected amplitudes `(U0, P0)`;
- symbolic solution of the post-leading flexural and membrane blocks;
- representative live clean checks that the membrane-mode visibility coefficient
  is nonzero on the active clean path.

**Result:**
- raw `im(D_rich,eta)` is not exactly preserved at the first checked
  post-leading order;
- a corrected one-parameter membrane thickening is preserved instead;
- the canonical selected leading trace remains exactly `im(D_amp)`.

**Current status:** **closed only at the first checked post-leading recurrence level**.


## A24. The membrane thickening direction is currently quotient-like, not canonically normalized away

**Statement.** After C3j, the project should not treat the extra membrane
thickening direction as already removed by a canonical local normalization.
At the checked order the corrected higher-order selected family is 3D, the
canonical `J_0` projection kills exactly one membrane line inside it, and the
current checked local data allow a whole family of 2D sections with the same
projected selected trace plane `im(D_amp)`. Therefore the best current local
selected object is the quotient of the corrected 3D family by that membrane
line.

**Checked:** yes, at the quotient / first higher-order kernel level.

**Verification used:**
- symbolic derivation in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- symbolic computation of the projection kernel on the corrected higher-order
  family;
- symbolic construction of the whole family of 2D sections, each still
  projecting to `im(D_amp)`;
- reuse of the C3i checked fact that the next recurrence layer does not kill the
  membrane line.

**Result:**
- no canonical local 2D normalization is presently justified;
- the membrane direction is best treated as quotient-like rather than as a
  proved gauge symmetry or a proved additional selected physical degree of
  freedom;
- the correct current theorem-facing local object is the quotient class modulo
  that membrane line.

**Current status:** **closed only at the quotient / first higher-order kernel level**.


## A25. No intrinsic canonical higher-order representative is currently justified beyond the membrane quotient

**Statement.** After C3k, the project should not assume that the current checked
local equations already pick a canonical representative of the membrane-quotient
class. The currently tested candidates either fail to distinguish
representatives, remain chart-dependent, or require an extra metric choice.
Therefore the best current local selected object is still the quotient of the
corrected 3D family by the membrane line.

**Checked:** yes, on the current checked local quotient boundary.

**Verification used:**
- symbolic derivation in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- symbolic check that the next checked compatibility layer does not distinguish
  representatives;
- symbolic check that the checked local residual vanishes along the membrane
  direction;
- symbolic quotient-preserving chart changes showing that `U1 = 0` is only a
  section choice;
- symbolic derivation that orthogonality / minimal-norm selectors depend on an
  extra metric.

**Result:**
- no intrinsic canonical higher-order representative is presently justified;
- the quotient object remains the strongest current theorem-facing local
  selected object;
- any future canonical representative theorem needs an additional intrinsic
  higher-order selector not yet derived.

**Current status:** **closed only on the current checked local quotient boundary**.


## A26. On the current checked local boundary the quotient object is final

**Statement.** After C3l, the project should treat the membrane quotient, not a
canonically normalized representative, as the final local theorem-facing
selected object on the current checked local boundary. This is because every
currently justified local selected invariant factors through that quotient and
no checked local condition distinguishes representatives inside one quotient
class.

**Checked:** yes, on the current checked local boundary.

**Verification used:**
- symbolic derivation in
  `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/formal_local_family_check.py`;
- symbolic factorization of the canonical `J_0` trace through the quotient map;
- symbolic check that the checked local residual vanishes identically on the
  corrected family;
- symbolic/structural confirmation that the next checked local compatibility
  layer adds no representative-level invariant;
- reuse of the C3k checked failure of the strongest plausible intrinsic
  selectors.

**Result:**
- Outcome B holds on the current checked local boundary;
- the membrane quotient is the final local theorem-facing selected object on
  that boundary;
- any future canonical representative theorem requires genuinely new local
  information beyond the current checked boundary.

**Current status:** **closed only on the current checked local boundary**.

