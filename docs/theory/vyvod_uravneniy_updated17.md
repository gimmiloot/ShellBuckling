# Вывод уравнений — обновлённая версия

## Статус документа

Этот файл разделён на три части:

- **Часть 1** — только то, что на текущем этапе считается достаточно надёжно установленным на уровне формул, структурных связей и постановок.
- **Часть 2** — только те численные и проектные выводы, которые действительно проверялись.
- **Часть 3** — наши рассуждения, интерпретации и рабочие гипотезы.

Во всех разделах отдельно указано, что **проверено**, а что **не проверено**.

---

# Часть 1. Зафиксированные формулы и постановки

## 1.1. Что считаем установленным без пересмотра

### 1.1.1. Старая reduced/full архитектура как основной путь исчерпана

На уровне проекта зафиксировано, что старые ветки
`F_min_reduced`, `F_min_full_v2`, `F_min_full_v3_chernykh`
не дали качественно нового критерия потери устойчивости.

Это не формула, а **зафиксированное исходное условие** для всех дальнейших выводов: новая постановка должна строиться уже **вне** старой 5D/6D philosophy.

**Проверено:** да, численно на серии тестов старой архитектуры.

**Не проверено:** не доказано в теоретическом смысле, что никакая модификация старой архитектуры в принципе не может сработать; зафиксирован только отрицательный результат уже выполненных веток.

---

## 1.2. Базовый новый operator class

### 1.2.1. Набор неизвестных

Новый mixed weak class строится на кинематических полях

```text
U = (u_s, u_n, v, varphi, psi)
```

и сопряжённых результантах

```text
P = (T_s, T_theta, S, Q_s, M_s, M_theta, H, chi).
```

Здесь:
- `u_s, u_n` — касательное и нормальное смещения в локальном базисе;
- `v` — окружное касательное смещение;
- `varphi` — меридиональный поворот;
- `psi` — окружной поворот;
- `S` — мембранный окружной shear-resultant;
- `Q_s` — меридиональная поперечная сила;
- `H` — twist-moment;
- `chi` — окружная поперечная сила.

Из этого следует, что новый минимальный окружной блок содержит две независимые пары:

```text
(v, S),   (psi, H, chi).
```

**Проверено:** да, как рабочая постановка mixed-weak ветки и как структура testbench/solver.

**Не проверено:** не доказано пока, что это уже окончательный минимальный полный набор для строгой статьи-уровня теории.

---

### 1.2.2. Corrected kinematics

Зафиксированы corrected-кинематические связи для осесимметрического фона:

```text
r' = e_s c_0 - lambda_s0 s_0 varphi,
z' = - e_s s_0 - lambda_s0 c_0 varphi.
```

Здесь

```text
c_0 = cos(varphi_0),
s_0 = sin(varphi_0),
kappa_s0 = varphi_0',
lambda_s0 = 1 + e_s0,
lambda_theta0 = r_0 / x,
kappa_theta0 = s_0 / r_0.
```

**Проверено:** да, как базовый corrected block проекта; именно с ним выполнялись все последующие mixed-weak построения.

**Не проверено:** не выполнена отдельная полная повторная перепроверка всех этих формул по общей теории оболочек от начала до конца в одном замкнутом тексте.

---

### 1.2.3. Corrected circumferential bending block

Как базовый сохраняется corrected circumferential bending block

```text
M_theta = nu M_s + (c_0/(12 mu^2 r_0)) varphi - (s_0/(12 mu^2 r_0^2)) r,
varphi' = Lambda (M_s - nu M_theta),
Lambda = 12(1-nu^2) mu^2.
```

**Проверено:** да, этот блок зафиксирован как обязательный и использовался в новой ветке.

**Не проверено:** не доказано пока в отдельном замкнутом тексте, что это уже окончательная запись без скрытых альтернативных перепараметризаций.

---

## 1.3. Кинематические меры нового класса

На фоне `Y_0 = (T_s0, Q_0, M_s0, r_0, z_0, varphi_0)` вводятся следующие меры:

```text
eps_s(U) = u_s' - kappa_s0 u_n,

eps_theta(U) = (c_0 u_s + s_0 u_n)/x + (n/x) v,

gamma_s theta(U) = v' - (r_0'/r_0) v - (n/x) u_s,

g_n(U) = u_n' + lambda_s0 varphi - kappa_s0 u_s,

kappa_s(U) = varphi'.
```

Также в новой ветке используется corrected circumferential curvature `kappa_theta^new(U)` и независимый twist/shear channel, содержащий `psi`, `H`, `chi`.

**Проверено:**
- `eps_s`, `eps_theta`, `gamma_s theta`, `g_n`, `kappa_s` — да, как рабочие определения нового класса;
- наличие независимого окружного twist/shear channel — да.

**Не проверено:** окончательно не доведена полностью строгая ковариантная запись коэффициентов при `psi`, `varphi` и `u_n` во всех curvature/shear формулах.

---

## 1.4. Weak-form и граничные пары

Новая постановка фиксируется как mixed weak-form, а не как один scalar potential:

```text
A_n(X, Xhat; q) = K_n(X, Xhat) - G_ps,n(X, Xhat; q) + B_partial,n(X, Xhat) = 0,
```

где `X = (U, P)`.

При этом на правой границе существенные/натуральные пары устроены так:

```text
(T_s, u_s), (Q_s, u_n), (S, v), (M_s, varphi), (H, psi).
```

Для используемой в mixed-weak testbench постановки с существенными условиями

```text
u_n(1) = 0,
varphi(1) = 0,
```

и свободными

```text
u_s(1), v(1), psi(1)
```

натуральные условия имеют вид

```text
T_s(1) = 0,
S(1) = 0,
H(1) = 0.
```

**Проверено:** да, как результат проверки conjugate pairs на краю.

**Не проверено:** не завершена ещё полная article-level derivation всей weak-form от начала до конца в одном тексте.

---

## 1.5. Prestress/load block

Prestress/load part нового класса **не** замыкается в scalar potential `G(U)`, а вводится как отдельная билинейная weak-form `G_ps`.

В рабочем виде использовался блок типа

```text
G_ps,n(X, Xhat; q)
```

с forcing-структурой, восстанавливаемой из corrected strong meridional/normal equations.

**Проверено:** да, на уровне структуры и testbench-логики.

**Не проверено:** не получена ещё окончательная строгая статья-уровня запись всего `G_ps` без промежуточных рабочих обозначений.

---

## 1.6. Центр-регулярность

Principal-part анализ нового mixed weak class даёт у центра следующий scaling:

```text
u_s, u_n, v = O(x^n),
varphi, psi = O(x^(n-1)),
T_s, S, T_theta = O(x^(n-1)),
Q_s, M_s, M_theta, H, chi = O(x^(n-2)).
```

Следствие: physical regular family снова двумерно, то есть для каждого `n` существуют две central regular modes.

**Проверено:** да, как результат principal-part анализа и как основа для построения `v2`-testbench.

**Не проверено:** не выполнено отдельное строгое доказательство единственности именно этого scaling среди всех возможных mixed extensions.

---

## 1.7. Целевой theorem-level объект для clean full `simple support / подвижный шарнир`

Для активной clean standalone full `simple support / подвижный шарнир` ветви
теперь нужно явно отделять:

1. **полный linearized mixed operator**, который должен задавать критичность;
2. **reduced boundary-only baseline** `B_mix`, который пока остаётся лишь raw
   working criterion;
3. **будущий theorem-level шаг equivalence**, который ещё не закрыт.

На уровне живой clean architecture полный дискретный mixed operator имеет вид

```text
L_full,n(q) = [A_int,n(q); B_full,n(q)],
```

где:

- `A_int,n(q)` — interior collocation block текущего mixed operator;
- `B_full,n(q)` — edge trace block с active critical rows
  `[u_n(1), varphi(1), T_s(1), S(1), H(1)]`.

В current clean center reduction используется матрица

```text
C_center,n(q) = [C_amp,n(q); C_reg,n(q)],
```

где

```text
C_amp(c) =
  [u_s/x^n,
   varphi/x^(n-1)] at x = x0,

C_reg(c) =
  [u_n/x^n + (lambda_c/n) varphi/x^(n-1),
   psi/x^(n-1) - lambda_c varphi/x^(n-1)] at x = x0.
```

Смысл этого разбиения такой:

- `C_reg(c)=0` — это именно admissible center-regular constraints;
- `C_amp(c)` — две свободные reduced center amplitudes;
- overall scaling не является частью theorem statement и фиксируется только при
  выборе координат на одном и том же двумерном admissible family.

Текущий solver строит span `V_reg,n(q)` из двух constrained modes. После
коэффициентной нормировки и ортогонализации это уже не буквально
center-normalized basis, поэтому для theory-facing редукции нужно использовать
canonical rebasing

```text
G_amp,n(q) = C_amp,n(q) V_reg,n(q),
V_adm,n(q) = V_reg,n(q) G_amp,n(q)^(-1),
```

если `det G_amp,n(q) ≠ 0`.

Тогда preferred reduced tangent operator имеет вид

```text
L_red,n(q) = [A_int,n(q); B_full,n(q)] V_adm,n(q).
```

Его boundary-only descendant:

```text
B_red,n(q) = B_full,n(q) V_adm,n(q),
```

а текущий raw clean object удовлетворяет relation

```text
B_mix,n(q) = B_red,n(q) G_amp,n(q).
```

Следовательно, на этом шаге как **theorem-level target object** проекта нужно
фиксировать не `B_mix` сам по себе, а nontrivial-kernel problem для полного
reduced operator `L_red,n(q)` на admissible center-regular space. Будущая
эквивалентность

```text
ker(L_red,n(q)) != {0}
```

с boundary-only degeneration `sigma_min(B_mix)=0` пока ещё **не доказана** и
должна оформляться как отдельный C3-обязательный шаг.

**Проверено:** на уровне repository derivation из live clean objects, через CAS
для block identities и через representative numerical checks в
`proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator`.

**Не проверено:**
- exact continuum-level kernel equivalence между полным clean mixed BVP и
  `L_red`;
- exact interior elimination step, при котором `A_int V_adm` должен перейти в
  нуль уже на theorem level, а не только в least-squares sense текущего кода;
- существование genuine quadratic form / second-variation object на том же
  reduced admissible space.

## 1.8. C3: что именно уже доказано для `L_red`, а что ещё нет

После фиксации объекта `L_red` нужно различать три уровня утверждений.

### 1.8.1. Полный admissible clean problem как theorem-level цель

Итоговая theorem-level цель проекта по-прежнему состоит в том, чтобы связать
критичность clean full `simple support / подвижный шарнир` задачи с
существованием нетривиального admissible center-regular возмущения в ядре
полного mixed operator.

На этом шаге **не доказано**, что текущий конечномерный span `V_adm` уже
исчерпывает всё это пространство admissible perturbations.

### 1.8.2. Текущий repo-selected reduced family

Для текущей live clean architecture можно точно определить лишь выбранное
двумерное reduced family

```text
A_repo,n(q) = im(V_adm,n(q)).
```

Здесь `V_adm` определяется из `V_reg` формулой

```text
V_adm = V_reg (C_amp V_reg)^(-1),
```

так что

```text
C_amp V_adm = I_2,
C_reg V_adm = 0.
```

Из этого немедленно следует:

- `V_adm` имеет полный столбцовый ранг 2, потому что имеет left inverse
  `C_amp` на своём image;
- отображение

```text
Phi_n,q : R^2 -> A_repo,n(q),
Phi_n,q(a) = V_adm,n(q) a
```

  является линейной биекцией;
- для любого `c = V_adm a` из `A_repo,n(q)` выполнено

```text
C_reg c = 0,
C_amp c = a.
```

То есть на выбранном reduced family reduced coordinates совпадают с двумя
center amplitudes.

### 1.8.3. Exact C3 kernel-equivalence, который уже можно фиксировать

Пусть

```text
L_full,n(q) = [A_int,n(q); B_full,n(q)],
L_red,n(q) = L_full,n(q) V_adm,n(q).
```

Тогда для любого `a in R^2` имеем точную конечномерную эквивалентность

```text
L_red,n(q) a = 0
iff
c := V_adm,n(q) a belongs to A_repo,n(q) ∩ ker(L_full,n(q)).
```

Эквивалентно,

```text
ker(L_red,n(q))  <->  A_repo,n(q) ∩ ker(L_full,n(q))
```

через биекцию `a -> V_adm a`.

Это и есть точный C3-результат текущего шага: `ker(L_red)` уже можно строго
идентифицировать с ядром полного оператора, **но только после ограничения на
текущий выбранный reduced family** `A_repo = im(V_adm)`.

### 1.8.4. Basis-independence и boundary-only descendants

Если `T in GL(2)` и `V_tilde = V_adm T`, то

```text
im(V_tilde) = im(V_adm),
L_tilde = L_full V_tilde = L_red T,
B_tilde = B_full V_tilde = B_red T.
```

Значит, nontrivial-kernel question для `L_red` не зависит от выбора basis на
том же reduced family.

Кроме того,

```text
V_reg = V_adm G_amp,
B_mix = B_full V_reg = B_red G_amp.
```

Поэтому при `det G_amp ≠ 0`

```text
ker(B_mix) = G_amp^(-1)(ker(B_red)).
```

Итак, `B_red` и `B_mix` несут одну и ту же boundary-only information на
`A_repo`, но это **не означает**, что они уже эквивалентны полному reduced
operator `L_red`.

### 1.8.5. Что именно остаётся открытым после C3

На этом шаге всё ещё **не доказано**:

- что `A_repo = im(V_adm)` совпадает с полным exact admissible center-regular
  tangent space clean mixed problem;
- что `ker(L_red)` эквивалентно `ker(B_red)`;
- что `ker(L_red)` эквивалентно raw boundary-only reading `ker(B_mix)` или
  `sigma_min(B_mix)=0`;
- что на том же space существует genuine quadratic form / second variation.

Единственное безусловное включение, которое уже можно писать немедленно:

```text
ker(L_red) ⊆ ker(B_red),
```

поскольку `B_red` есть boundary block внутри stacked operator `L_red`.

## 1.9. C3b: что именно означает losslessness и что сейчас реально закрыто

После C3 следующий вопрос нельзя формулировать расплывчато. Здесь нужно
разделять три разных пространства.

### 1.9.1. Theorem-facing full admissible space

Искомое theorem-level пространство для clean full
`simple support / подвижный шарнир` задачи — это пространство всех
center-regular perturbations полного linearized mixed problem до наложения
окончательного критического edge condition. Обозначим его

```text
A_full^th,n(q).
```

На текущей repository boundary это пространство **не закрыто как отдельный
готовый объект**: нет ещё article-level local solution-family derivation,
которая бы прямо отождествляла его с текущим конечномерным construction.

### 1.9.2. Что current code знает точно: weighted trial space и center constraints

Current code задаёт weighted polynomial trial space коэффициентов

```text
X_trial,n = R^N,
N = 8 * m_basis,
```

через `TrialSpace` и `field_exponent(...)`. Для него степени у центра уже
зашиты прямо в basis:

```text
u_s, u_n, v ~ x^n,
varphi, psi, T_s ~ x^(n-1),
Q_s, M_s ~ x^(n-2).
```

Поэтому на уровне current ansatz principal-part scaling уже встроен.

Явное coefficient-level center-regular constraint space внутри этого ansatz:

```text
W_reg,n(q) = { c in X_trial,n : C_reg,n(q) c = 0 }.
```

### 1.9.3. Leading center data действительно двумерны

Поскольку basis functions имеют вид

```text
x^p * t^k,   t = (x - x0)/(1 - x0),
```

а `t(x0)=0`, в leading center data участвуют только `k=0` coefficients.
Следовательно, на leading amplitudes

```text
(a_us, a_un, a_phi, a_psi)
```

матрица `C_center` имеет точный block

```text
[1  0      0       0]
[0  0      1       0]
[0  1  lambda_c/n  0]
[0  0   -lambda_c  1].
```

Отсюда:

- `det(C_center,lead) = -1`, то есть full leading block имеет rank `4`;
- `C_reg,lead` имеет rank `2`;
- regular leading family задаётся двумя free amplitudes `(a_us, a_phi)`, а
  остальные leading coefficients определяются формулами

```text
a_un = -(lambda_c/n) a_phi,
a_psi = lambda_c a_phi.
```

Итак, current repository действительно знает, что **leading admissible center
data** двумерны.

### 1.9.4. Почему этого ещё недостаточно для losslessness

Это двумерное утверждение относится только к leading center data. Оно **не**
означает, что всё coefficient-level пространство `W_reg = ker(C_reg)` уже
двумерно.

На текущем active trial basis (`N = 48` при `m_basis = 6`) имеем:

```text
rank(C_reg) = 2,
dim ker(C_reg) = 46,
rank(C_center) = 4,
dim ker(C_center) = 44.
```

Значит, одного условия `C_reg c = 0` недостаточно, чтобы получить current
two-dimensional reduced family. Следовательно, `A_repo` нельзя отождествлять с
полным center-regular coefficient space только по center constraints.

### 1.9.5. Что current repo-selected family означает на самом деле

Current solver выбирает не всё `W_reg`, а специальное двумерное семейство,
определяемое constrained regularized least-squares rule:

```text
minimize ||A_int c||^2 + reg ||c||^2
subject to C_center c = [a_1, a_2, 0, 0].
```

Если обозначить через `M_amp,n(q)` coefficient block соответствующего KKT map,
то exact current selected family inside the weighted ansatz равно

```text
A_ls,n(q) = im(M_amp,n(q)).
```

Именно это пространство current repository фактически использует как reduced
family; после normalization / orthogonalization и canonical rebasing оно даёт

```text
A_repo,n(q) = im(V_adm,n(q)) = A_ls,n(q)
```

на уровне current ansatz/construction.

### 1.9.6. Точный результат C3b

На этом шаге можно честно зафиксировать:

1. `A_repo = im(V_adm)` **не** равно всему `ker(C_reg)`; оно является только
   special 2D subfamily внутри much larger trial coefficient space.
2. `A_repo` уже можно точно идентифицировать с current KKT-selected amplitude
   family `A_ls = im(M_amp)` внутри weighted trial ansatz.
3. Равенство

```text
A_repo,n(q) = A_full^th,n(q)
```

   всё ещё **не доказано**.

То есть reduction уже lossless относительно **current repo-selected
constrained-LS family**, но ещё не lossless относительно полного theorem-facing
clean admissible tangent space.

### 1.9.7. Exact missing ingredient после C3b

Чтобы получить настоящее theorem-level losslessness, нужен следующий шаг,
которого в repository пока нет:

- либо article-level derivation / theorem, что full clean center-regular local
  solution family действительно двумерно и полностью parameterized текущими
  two leading amplitudes в том смысле, который совместим с `M_amp`;
- либо отдельное completeness statement, что current weighted trial +
  constrained-LS construction не теряет admissible perturbations из
  `A_full^th`.

Именно этот шаг, а не ещё одна численная refinement-проверка, сейчас остаётся
главным theorem-level bottleneck после C3b.

## 1.10. Continuum/local completeness step: что удаётся вывести из current mixed equations

Следующий theorem-facing вопрос после C3b теперь можно формулировать так:

```text
совпадает ли A_full^th,n(q) с A_ls,n(q) = im(M_amp,n(q)) = im(V_adm,n(q))?
```

На текущей repository boundary полный continuum/local proof этого равенства
всё ещё не получен. Но current mixed equations позволяют продвинуться на один
слой глубже: вывести local **leading-order** clean center-regular family
непосредственно из principal center block, а не только из current trial-space
ansatz.

### 1.10.1. Current principal center model

Для local-leading derivation current repository использует тот же principal
center model, который уже неявно зашит в active center reduction:

```text
c_0 -> 1,
s_0 -> 0,
a_0 -> 1/x,
a_0' -> -1/x^2,
lambda_s0 -> lambda_c,
lambda_theta0 -> 1,
```

а поля записываются в regular orders

```text
u_s = A_us x^n,
u_n = A_un x^n,
v   = A_v x^n,
varphi = A_phi x^(n-1),
psi    = A_psi x^(n-1),
T_s    = A_Ts x^(n-1),
Q_s    = A_Qs x^(n-2),
M_s    = A_Ms x^(n-2).
```

Это уже не pure finite-basis statement, а local principal-part model для
continuum mixed equations в current repository sense.

### 1.10.2. Что даёт leading singular block

Из leading parts `R_un`, `R_gtheta`, `R_phi`, `R_us` получаются relations:

```text
A_un = -(lambda_c / n) A_phi,
A_psi = lambda_c A_phi,
A_Ms  = ((n + nu - 1) + nu n lambda_c) A_phi / (Lambda (1 - nu^2)),
```

и одна linear relation, связывающая `A_Ts` с `A_us` и `A_v`.

Следовательно, на уровне local **leading-order** continuum family свободными
остаются те же две amplitudes

```text
(A_us, A_phi),
```

которые current repository already uses in `C_amp`.

Итак, теперь можно честно зафиксировать:

- continuum/local leading regular family действительно двумерно в current
  principal center model;
- current ansatz-level amplitudes совпадают с amplitudes этого local-leading
  family.

### 1.10.3. Почему этого всё ещё недостаточно для theorem-level losslessness

Когда пытаются замкнуть не только `R_un`, `R_gtheta`, `R_phi`, `R_us`, но и
весь frozen principal truncation (`R_Ts`, `R_v`, `R_Qs`, `R_Ms`) на том же
leading-level model, nontrivial closed family не получается.

То есть current repository now knows:

1. local **leading-order** clean center-regular family is two-parameter;
2. `A_ls` matches that family at leading amplitude level;
3. но full local formal-completeness theorem всё ещё требует следующего слоя:
   regular-singular recurrence / higher-order center expansion of the continuum
   mixed system.

### 1.10.4. Точный результат этого шага

Поэтому на этом шаге можно утверждать только следующее:

- full equality

```text
A_full^th,n(q) = A_ls,n(q)
```

  всё ещё **не доказано**;
- proved stronger intermediate statement:
  current continuum/local principal center model has a two-parameter
  leading-order clean admissible family parameterized by the same amplitudes as
  `A_ls`;
- exact missing step:
  prove the higher-order local regular-singular continuation/completeness
  theorem and only then compare that full local family with the global
  weighted-trial KKT-selected family.

### 1.10.5. Higher-order recurrence inside the fully frozen principal model

Следующий шаг после 1.10.4 был уже не про один singular leading block, а про
полную frozen principal layer-by-layer систему на тех же scaling orders

```text
u_s = U0 x^n + U1 x^(n+1) + U2 x^(n+2),
u_n = N0 x^n + N1 x^(n+1) + N2 x^(n+2),
v   = V0 x^n + V1 x^(n+1) + V2 x^(n+2),
varphi = P0 x^(n-1) + P1 x^n + P2 x^(n+1),
psi    = Y0 x^(n-1) + Y1 x^n + Y2 x^(n+1),
T_s    = T0 x^(n-1) + T1 x^n + T2 x^(n+1),
Q_s    = Q0 x^(n-2) + Q1 x^(n-1) + Q2 x^n,
M_s    = M0 x^(n-2) + M1 x^(n-1) + M2 x^n,
```

при тех же frozen background replacements

```text
c0 -> 1,
s0 -> 0,
a0 -> 1/x,
a0' -> -1/x^2,
lambda_s0 -> lambda_c,
lambda_theta0 -> 1,
```

и без возврата omitted finite center coefficients `kappa_s0`, `kappa_theta0`,
`g_s`, `g_n`.

На этом уровне выясняется важная поправка к 1.10.2: two-parameter object
`(A_us, A_phi)` относится только к singular leading block, но не к полной
frozen principal layer system.

### 1.10.6. Точный finite-order result для fully frozen principal model

Если собрать полный leading layer из

```text
R_us, R_un, R_Ts, R_gtheta, R_phi, R_Ms, R_v,
```

то его determinant в physical substitution имеет вид

```text
delta_leading =
  n^2 (2n - 1) (2n + 1)
  [lambda_c n nu^3 - lambda_c n nu^2 + lambda_c n
   - 2 lambda_c nu^3 + 2 lambda_c nu^2 + lambda_c nu - 3 lambda_c
   - n nu^3 + n nu^2 + n nu - 2]
  / [2 (nu + 1)].
```

Поэтому при generic nonresonance full frozen principal leading layer forces

```text
U0 = V0 = T0 = N0 = P0 = Y0 = M0 = 0.
```

После этого next layer уже не invertible как full `8 x 8` system: its rank is
`7`, nullity is `1`, and the generic solution is

```text
N1 = P1 = Y1 = M1 = Q0 = 0,
U1 = T1 (-n nu - n - 2 nu + 2) / (-n^2 + n + 2),
V1 = T1 (n nu + n + 4) / (-n^2 + n + 2),
```

so one membrane parameter `T1` remains free. The denominator reveals the same
special resonance location

```text
(n - 2)(n + 1) = 0.
```

After substituting this generic next-layer membrane mode, the checked second
layer becomes invertible again, with physical determinant

```text
delta_second =
  -3 n^2 (2n + 1) (2n + 3)
  [lambda_c n^2 nu + lambda_c n^2
   - 2 lambda_c n nu^3 + 2 lambda_c n nu^2 + 3 lambda_c n nu - 3 lambda_c n
   + n^2 nu + n^2 + 2 n nu^3 - 2 n nu^2 + n nu + 7 n
   + 4 nu^3 - 4 nu^2 - 2 nu + 10]
  / [2 (nu + 1)],
```

and the checked second-layer coefficients are uniquely zero:

```text
U2 = N2 = V2 = P2 = Y2 = T2 = M2 = Q1 = 0.
```

Representative live clean evaluation on `n = 4, 6, 7, 8` with honest
`lambda_c = lambda_s0(x0)` confirms that `delta_leading`, the next flexural
subdeterminant, and `delta_second` are all far from zero on the active
competition set.

Следовательно, на текущем repository boundary можно зафиксировать только более
жёсткое formula-level statement:

1. singular leading block действительно дает two-amplitude compatibility data;
2. full fully frozen principal model через проверенные finite orders **не**
   реализует ожидаемое clean two-amplitude local family;
3. значит, следующий theorem-facing шаг — не продолжать тот же fully frozen
   principal truncation, а вернуть первые omitted finite center coefficients /
   forcing terms и уже на richer local model выводить regular-singular
   recurrence.

### 1.10.7. C3c: richer local center model with first omitted finite coefficients

На этом шаге richer local model берётся уже не в fully frozen principal виде,
а с первыми honest finite center corrections of the clean background:

```text
c0 = 1 + O(x^2),
s0 = K x + O(x^3),
a0 = 1/x + O(x),
a0' = -1/x^2 + O(1),
lambda_s0 = lambda_c + O(x^2),
lambda_theta0 = lambda_c + O(x^2),
kappa_s0 = K + O(x^2),
kappa_theta0 = K / lambda_c + O(x^2),
T_s^0 = T_s^0(0) + O(x^2),
T_theta^0 = T_theta^0(0) + O(x^2),
M_theta^0 = M_theta^0(0) + O(x^2),
T_sn^0 = Q1 x + O(x^3).
```

Honest background recurrence fixes the first omitted coefficients
`Ts2, U3, K3, Ms2, Q3` uniquely. Для C3c критична не столько сама громоздкая
CAS-формула для каждого из них, сколько их order: все эти corrections начинают
влиять только с `O(x^2)` / `O(x^3)`.

Ключевое observation теперь такое: restored first-finite background terms не
могут изменить тот obstruction layer, который уже виден в `R_Ts`, `R_Ms`, и
`R_v`.

1. In `R_Ts`, decisive low-order term comes from
   `-(s0 c0 / r0^2) Mtheta ~ x^(-1) x^(n-2) = x^(n-3)`.
   Restored corrections change `s0 c0 / r0^2` only by `O(x)`, so they first
   enter this row only at `x^(n-1)`.
2. In `R_Ms`, the low layer comes from `Ms_x`, `a0 M_s`, `-a0 M_theta`, `-Q_s`,
   and `(n/x) H`, again at `x^(n-3)`. First restored finite background terms
   also reach this row only at `x^(n-1)` or higher.
3. In `R_v`, the obstruction layer comes from `kappa_theta0 chi` with
   `chi ~ x^(n-3)`. Since `kappa_theta0 = K / lambda_c + O(x^2)`, restored
   terms again start only at `x^(n-1)`.

Значит, after the same singular leading relations

```text
N0 = -(lambda_c / n) P0,
Y0 = P0,
M0 = (n - 1) P0 / [12 mu^2 (1 - nu^2)^2],
```

низкоуровневые obstruction rows остаются exactly the same as in the
constant-finite model:

```text
R_Ts[-1] = -K P0 [lambda_c n nu - lambda_c nu + n + 1]
           / [12 lambda_c^3 mu^2 (1 - nu^2)^2],

R_Ms[-1] = -P0 [ ... ] / [12 lambda_c mu^2 (1 - nu^2)^2],

R_v[-1]  =  K P0 n [ ... ] / [12 lambda_c^4 mu^2 (1 - nu^2)^2].
```

Уже simplest factor in `R_Ts[-1]` enough for the active clean regime:

```text
lambda_c n nu - lambda_c nu + n + 1
= lambda_c nu (n - 1) + n + 1 > 0
```

for `lambda_c > 0`, `nu > 0`, `n >= 4`.

Поэтому whenever `K != 0`, richer first-finite layer still forces

```text
P0 = 0.
```

Representative live clean evaluation on `n = 4, 6, 7, 8` confirms that the
center curvature `K = kappa_s0(x0)` is nonzero and all three obstruction
factors are far from zero on the active competition set.

Итак, C3c closes only the following conservative statement:

1. first omitted finite center coefficients were restored honestly;
2. but they do **not** change the decisive low-order obstruction layer;
3. so they do **not** restore the expected clean two-amplitude local family;
4. consequently `A_full^th = A_ls` is still not proved.

Следующий theorem-facing шаг теперь уже уже не формулируется как simply
"restore the first omitted finite coefficients". Эти coefficients уже checked
and are insufficient. Нужен local ingredient, который может действовать на тех
же lowest obstruction orders, или же нужен пересмотр того, что именно project
должен считать theorem-facing local comparison object.
# Часть 2. Проверенные численные и проектные выводы

## 2.1. Что уже проверено по старой архитектуре

Проверенные отрицательные результаты:

1. Простая замена background в старом классе недостаточна.
2. Частичный ремонт старого 5D/6D оператора qualitative shift не дал.
3. Проблема не сводится к одной closure-формуле и не сидит только в крае.

**Проверено:** да, на серии старых solver-веток и логов проекта.

**Не проверено:** не доказано, что абсолютно любой старый 5D/6D variant невозможен; зафиксировано только, что уже рассмотренные варианты не сработали.

---

## 2.2. Что проверено по новой mixed-weak ветке

### 2.2.1. Проверено структурно

На новой mixed-weak ветке проверено следующее:

1. Residual-based weak-form даёт неправильные conjugate pairs на краю и поэтому отбракована.
2. Functional-route является рабочим направлением.
3. По вариации по `Q_s` восстанавливается corrected normal-kinematic constraint.
4. Независимые окружные каналы `(v,S)` и `(psi,H,chi)` реально входят в новую постановку и не являются чисто декоративными.
5. Right boundary matrix должна строиться из двух **central regular modes**, а не из глобального surrogate interior-ядра.

**Проверено:** да.

**Не проверено:** пока не завершена финальная BVP-реализация, которая воспроизводила бы этот результат уже не на surrogate-testbench, а в окончательном solver’е.

---

### 2.2.2. Проверено численно для `B_mix`

Зафиксирована boundary matrix

```text
B_mix(q) = [[u_n^(1)(1), u_n^(2)(1)],
            [varphi^(1)(1), varphi^(2)(1)],
            [T_s^(1)(1),   T_s^(2)(1)],
            [S^(1)(1),     S^(2)(1)],
            [H^(1)(1),     H^(2)(1)]].
```

Рабочий критерий в новой ветке:

```text
sigma_min(B_mix(q)) = 0.
```

**Проверено:**
- сама формулировка и её вычислимость в testbench — да;
- полная строгость критерия как окончательной теории — нет.

---

## 2.3. Проверенный текущий mixed-weak кандидат на критическую нагрузку

После resolution study, fine scan, adaptive tracking и ultra-fine targeted scan на mixed-weak ветке получен устойчивый кандидат:

```text
n_cr = 13,
q_cr^(13) ≈ 3.79..3.80 MPa.
```

Ближайшая конкурентная ветвь:

```text
n = 14,
q_cr^(14) ≈ 4.28 MPa.
```

Поэтому в рамках **только mixed-weak exploratory ветки** текущий лучший кандидат был

```text
q_cr ≈ 3.79..3.80 MPa,
n_cr = 13.
```

**Проверено:** да, как устойчиво локализованный численный результат в surrogate/testbench-ветке.

**Не проверено:**
- это не доказано как точное значение;
- `sigma_min` в точке минимума не дошло до машинного нуля;
- этот результат нельзя считать окончательным для полной задачи `simple support`, потому что background и критическое возмущение тогда ещё были не полностью согласованы.

---

## 2.4. Что проверено по полной задаче simple support

К настоящему моменту надёжно установлено следующее.

### 2.4.1. Полная задача simple support ещё не решена

Ранее полученные “simple support” результаты в mixed-weak ветке были получены не для полностью согласованной задачи, потому что:
- осесимметрический фон оставался старым рабочим background;
- simple support вводился только на уровне критического критерия / boundary matrix.

**Проверено:** да, это установлено разбором используемой архитектуры.

**Не проверено:** окончательная полная simple-support mixed-weak реализация пока не построена.

---

### 2.4.2. Для осесимметрической simple-support задачи по названиям BC выбраны корректные условия

Для осесимметрического фона в непологой постановке как естественный набор simple-support условий рассматривались:

```text
в центре:   T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
на краю:    T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

По **названиям условий** и по их физическому смыслу этот выбор был признан корректным рабочим кандидатом.

**Проверено:** да, на уровне интерпретации по названиям BC.

**Не проверено:** пока не доказано окончательно, что именно этот набор в текущих смешанных переменных полностью эквивалентен FEM-реализации simple support без скрытых различий в переводе условий.

---

### 2.4.3. Separate 6-state simple-support continuation уже проходит выше старого барьера, но физический потолок ветви остаётся открытым

К текущему моменту по separate full-state simple-support path нужно различать
несколько численных маркеров:

- old-path reproducible anchor: `4.3434 MPa`;
- old-path first persistent failure: `4.3440 MPa`;
- bounded pilot-20 ceiling для `u_z`-scaled state: `4.3520 MPa`;
- bounded audited pilot-21 ceiling для `u_z`-scaled continuation + auxiliary arc-like control: `4.3800 MPa`.

Поверх этого теперь существует быстрый checkpointed continuation + pointwise
confirm workflow на тех же уравнениях и тех же BC, который уже довел
operational continuation evidence до `6.0000 MPa`. Для `4.4000 MPa` при этом
уже выполнен более строгий milestone-audit: две независимые pointwise
confirm-проверки остаются near-reproducible на одном и том же accepted seed,
не показывают branch-jump suspicion и не дают short failure probe через
`4.4100 MPa`, но strict reproducibility пока все еще не закрыт, поэтому
`4.4000 MPa` не продвигается как новый canonical audited ceiling.

Более высокие sparse milestone-confirm на `5.0000`, `5.5000` и `6.0000 MPa`
тоже идут по тому же accepted seed, не показывают branch-jump suspicion и не
дают short failure probe через `6.0040 MPa`, однако выше `5.0 MPa` уже не
попадают под текущий near-reproducible threshold: repeat-solve drift растет
плавно, остается малым и заметно меньше обычного соседнего continuation-step
расхождения, но выходит выше текущего confirm-порога. Поэтому и эти точки пока
следует читать как operational continuation evidence, а не как новый audited
ceiling.

Этот набор фактов относится к **текущей численной реализации continuation- и
confirm-алгоритмов**, а не автоматически к физической критической нагрузке.

**Проверено:** да, по серии dedicated proof pilots и checkpointed fast/confirm run.

**Не проверено:** не доказано, что достигнутый на сегодня operational ceiling
совпадает с физической предельной точкой осесимметрической ветви.

---

### 2.4.4. Ни old-path барьер около `4.344 MPa`, ни ранние срывы около `4.36 MPa` нельзя считать физическим критическим давлением

Зафиксировано, что FEM для той же задачи дает критическую нагрузку порядка
`10 MPa`, а в литературе по круглым пластинам и annular plates отдельно
подчеркивается, что при hinged support и больших нагрузках уравнения пологих
оболочек хуже описывают докритическое состояние и требуется более общая
shell-theory постановка.

Кроме того, сам continuation ceiling заметно меняется без изменения equations и
без изменения simple-support BC set: old-path дает `4.3434 / 4.3440 MPa`,
pilot 20 поднимает bounded ceiling до `4.3520 MPa`, pilot 21 — до
`4.3800 MPa`, а новый checkpointed fast workflow локально идет до `6.0000 MPa`
и не показывает bounded failure даже в short confirm probes через `6.0040 MPa`.
Для `4.4000 MPa` уже есть более строгий near-reproducible milestone-audit без
branch-jump suspicion, а для `5.0000`, `5.5000` и `6.0000 MPa` confirm по
той же ветви остается same-seed и no-branch-jump, но выходит за текущий
near-reproducible threshold из-за малого гладкого drift'а repeat solve.

Следовательно, ни старый барьер около `4.344 MPa`, ни более ранние неудачи
около `4.36 MPa` нельзя интерпретировать как надежно найденную физическую
точку потери устойчивости. Текущий reading барьера остается прежде всего
численным / conditioning-related; дополнительно теперь видно, что открытым
остается и вопрос о том, насколько сама confirm-метрика для strict audit
согласована с наблюдаемым smooth same-branch drift.

**Проверено:** да, как проектный вывод.

**Не проверено:** не локализовано окончательно, что именно ломается первым —
перевод BC в переменные, сам осесимметрический BVP, continuation-алгоритм или
слишком жесткая audit-policy для repeat solve; не доказано и то, что текущая
ветвь действительно продолжается до физического предела без скрытого branch
change.

---

# Часть 3. Рассуждения, интерпретации и рабочие гипотезы

## 3.1. Почему mixed-weak кандидат `3.79..3.80 MPa` нельзя считать окончательным для simple support

Наше текущее рассуждение такое:

1. mixed-weak ветка действительно дала качественно новую картину по сравнению со старой architecture;
2. но в той версии задачи simple support ещё не был реализован как **полностью согласованный фон + критическое возмущение**;
3. поэтому значение

```text
q_cr ≈ 3.79..3.80 MPa
```

следует хранить как **exploratory mixed-weak candidate**, а не как окончательный результат для полной задачи `simple support`.

Это не опровержение mixed-weak ветки; это ограничение на интерпретацию её текущего численного результата.

---

## 3.2. Наиболее вероятный источник проблемы в полной simple-support задаче

Наиболее вероятная рабочая гипотеза сейчас такая:

- проблема сидит не в самих названиях BC;
- проблема сидит либо в переводе этих BC в текущие смешанные переменные осесимметрического solver’а,
- либо в том, что сам осесимметрический BVP для simple support численно намного жёстче старого background,
- либо в том, что текущий continuation по `solve_bvp` теряет нужную ветвь до реальной физической критической точки.

Это именно гипотеза, а не доказанный факт.

---

## 3.3. Почему переход к полной simple-support задаче обязателен

Если считать задачу физически последовательно, то нужно, чтобы:

1. докритический осесимметрический фон считался уже с simple-support закреплением;
2. критическое неосесимметрическое возмущение строилось на этом же фоне;
3. критерий потери устойчивости использовал те же BC.

Иначе получается численный тест чувствительности критерия к изменению boundary matrix, а не полная постановка задачи.

Это и есть причина, почему сейчас главным открытым местом проекта становится именно **осесимметрический simple-support background**.

---

## 3.4. Рабочий следующий шаг

Самый логичный следующий шаг — не пытаться сразу снова искать `q_cr`, а сначала добиться устойчивого решения именно осесимметрической задачи с simple support:

```text
(T_s, T_sn, M_s, u_r, u_z, varphi)
```

с BC

```text
T_sn(x0)=0, u_r(x0)=0, varphi(x0)=0,
T_s(1)=0, M_s(1)=0, u_z(1)=0.
```

Сначала хотя бы на фиксированных нагрузках, затем continuation.

Пока этого нет, любые новые оценки критической нагрузки для полной simple-support задачи будут преждевременными.

---

## 3.5. Промежуточная итоговая позиция проекта

На текущий момент проект разбивается на две линии:

### Линия A. Mixed-weak criterion
- теоретически сформулирован;
- численно дал содержательный exploratory candidate;
- остаётся основным новым направлением проекта.

### Линия B. Полная simple-support задача
- логически обязательна;
- на текущий момент не закрыта;
- требует отдельной стабилизации осесимметрического background solver’а.

Именно поэтому сейчас нельзя сливать эти две линии в одно окончательное утверждение о критической нагрузке.

---

## 3.6. Минимальная рабочая формулировка на сегодня

На сегодня наиболее аккуратная формулировка такая:

> Mixed-weak ветка уже показала, что старая reduced/full architecture недостаточна и что независимые окружные каналы действительно меняют картину критерия. Однако полная физически согласованная задача `simple support` ещё не доведена до устойчивого осесимметрического background, поэтому окончательная критическая нагрузка для этой постановки пока не считается найденной.

---

## Источники, на которые опирался этот файл

- `vyvod_uravneniy_V16_mixed_weak_criterion.txt`
- `project_journal_updated14.md`
- `mixed_weak_solver_v1.py`
- `mixed_weak_boundary_matrix_test_v2.py`
- `proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/pilot_23_clean_simple_support_reduced_tangent_operator.md`
- `Huang 1964 - Unsymmetrical Buckling of Thin Shallow.pdf`
- `holm3.pdf`
- `BauerVoronkovaSemenov-vestnik2022_1.pdf`
