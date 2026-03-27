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
  current KKT-selected amplitude family на representative clean points.

**Результат проверки:** текущий repository теперь знает следующее точно:
- leading admissible center data действительно двумерны;
- `A_repo = im(V_adm)` совпадает с exact current KKT-selected amplitude family
  внутри weighted trial ansatz;
- но `A_repo` не равно всему coefficient-level space `ker(C_reg)`, и equality
  между `A_repo` и full theorem-facing clean admissible tangent space пока не
  доказана.

**Текущий статус:** **не подтверждено как theorem-level факт; закрыто только ansatz-level characterization текущего selected family**.

## Короткая сводка по статусам

### Подтверждено / частично подтверждено
- A3, A4, A5, A6, A7, A10, A12, A13, A15, A16.

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
