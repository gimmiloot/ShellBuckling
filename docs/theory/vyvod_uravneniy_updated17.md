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
### 1.10.8. Что именно теперь нужно сравнивать с `A_ls`

После C3c вопрос больше нельзя читать как

```text
«совпадает ли current A_ls со всей unrestricted local center-regular family?»
```

без дополнительного уточнения. На этом месте нужно различать как минимум
четыре candidate objects:

1. `O1`: полное local center-regular formal family current clean mixed
   equations;
2. `O2`: то же family + лишь admissibility / normalization;
3. `O3`: local center-regular family + weak/interior residual-minimizing or
   KKT-type selection;
4. `O4`: local germ family, получающаяся как center trace глобально selected
   weak family, которую current repository фактически использует.

Новый helper
`proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`
показывает, что в live clean code `A_ls` означает не просто chart для regular
center data.

Для каждого amplitude vector `a = (a1, a2)` current weighted ansatz содержит
full affine fiber

```text
F_n,q(a) = { c in X_trial,n : C_center,n(q) c = [a1, a2, 0, 0] }.
```

Current repository family есть образ unique constrained minimizer

```text
c*(a) = argmin ( ||A_int,n(q) c||^2 + reg ||c||^2 )
        subject to C_center,n(q) c = [a1, a2, 0, 0].
```

То есть при

```text
H_n,q = A_int,n(q)^T A_int,n(q) + reg I
```

имеем KKT stationarity

```text
H_n,q c*(a) + C_center,n(q)^T lambda(a) = 0,
```

а значит для любого fiber direction `z in ker(C_center)` выполнено

```text
z^T H_n,q c*(a) = 0.
```

Иначе говоря, `A_ls = im(M_amp)` — это `H_n,q`-minimal section гораздо более
широкого amplitude fiber, а не просто «все center-regular local solutions».

Representative checks на active clean competition set `(n, q) = (4, 11.1),
(6, 17.6), (7, 17.3), (8, 17.8)` дают:

- `dim X_trial = 48`, `rank(C_center) = 4`, значит fixed-amplitude fiber остаётся
  `44`-мерным;
- KKT-selected map satisfies center constraints and fiber-orthogonality to
  numerical tolerance;
- простой constraint-only feasible reference имеет full objective больше на
  факторы порядка `10^6 .. 10^11`;
- если заменить full interior block `A_int` только first `5%`, `10%`, `20%`
  или `50%` collocation rows, получающийся selected map сильно меняется и не
  reproduces full-selection result.

Отсюда следует conservative reading:

- `O1` теперь выглядит слишком широким как direct comparison object для `A_ls`,
  потому что забывает already-present weak/interior selection layer;
- `O2` тоже недостаточен, если admissibility сама не кодирует тот же selection,
  а current repo этого не показывает;
- `O3` — наиболее plausibly correct local object, если настаивать именно на
  genuinely local theorem-facing formulation;
- `O4` ещё ближе к live architecture, потому что current selection строится из
  full interior operator `A_int`, а не только из center germs.

Значит, текущий theorem-facing bottleneck после C3c лучше формулировать так:

```text
нужно либо вывести selected local object, matching KKT/global weak selection,
либо доказать global-to-local theorem, что именно local trace of the selected
weak family является correct comparison object.
```

Следовательно, main missing theorem теперь уже не выглядит как raw local
completeness theorem for `O1`. Нужна теорема о selection/comparison object.

### 1.10.9. C3e: какой local selected object теперь разумно сравнивать с `A_ls`

После object-selection stage и C3e полезно явно разделить три объекта:

1. `A_reg^loc` — raw local center-regular formal family clean mixed equations;
2. `A_ls` — current global weighted-trial KKT-selected family live clean code;
3. `A_sel^loc` — theorem-facing local selected object, который должен
   сравниваться с `A_ls`, если сравнение вообще формулируется на local/germ
   языке.

Live clean architecture теперь позволяет выписать `A_ls` точнее. Обозначим

```text
C_center,n(q) = [C_amp,n(q); C_reg,n(q)],
D_amp = [[I_2], [0]],
H_n,q = A_int,n(q)^T A_int,n(q) + reg I.
```

Тогда полный selected center-data lift задаётся формулой

```text
P_sel,n(q) = H_n,q^(-1) C_center,n(q)^T
             (C_center,n(q) H_n,q^(-1) C_center,n(q)^T)^(-1),
```

и удовлетворяет

```text
C_center,n(q) P_sel,n(q) = I_4.
```

Его образ

```text
X_sel,n(q) = im(P_sel,n(q))
```

есть 4-мерный `H_n,q`-orthogonal lift полного center-data space. Current
selected family then reads as the regularity-zero amplitude slice

```text
A_ls,n(q) = im(P_sel,n(q) D_amp)
          = { c in X_sel,n(q) : C_reg,n(q) c = 0 }.
```

Значит, сами center constraints фиксируют только affine fiber

```text
F_n,q(a) = { c : C_center,n(q) c = [a1, a2, 0, 0] },
```

который в current weighted trial space остаётся 44-мерным. То, что превращает
этот fiber в current 2D family `A_ls`, есть не raw regularity, а глобальный
weak/KKT selection: unique `H_n,q`-minimal representative in each fiber.

Обновлённый helper
`proof_pilots/pilot_23_clean_simple_support_reduced_tangent_operator/selection_object_check.py`
проверяет на representative active clean points `(n, q) = (4, 11.1), (6,
17.6), (7, 17.3), (8, 17.8)`, что:

- `rank(C_amp) = 2`, `rank(C_reg) = 2`, `rank(C_center) = 4`, так что fixed-
  amplitude fiber действительно остаётся 44-мерным inside 48D trial space;
- KKT-selected 4D lift satisfies `C_center P_sel ≈ I_4` и expected
  `H`-orthogonality to `ker(C_center)`;
- amplitude slice `im(P_sel D_amp)` matches the current selected family;
- near-center-only surrogate objectives still do not reproduce the same
  selected map.

Отсюда следует более sharp conservative reading.

1. По умолчанию больше не следует сравнивать `A_ls` со всей raw family
   `A_reg^loc`.
2. Лучший точно определённый faithful candidate для theorem-facing local object,
   который сейчас реально виден в repo, есть

```text
A_sel,trace^loc := J_0(A_ls),
```

   то есть local germ / center trace глобально selected family.
3. Более сильный intrinsic object `A_sel,weak^loc` внутри `A_reg^loc`,
   определяемый через canonical local weak/KKT-type selection rule, пока не
   выведен.

Итак, C3e закрывает только делимитирующее утверждение:

```text
correct theorem-facing comparison object should already be selected,
and the best exact current candidate is the local trace of the globally
selected family, not the unrestricted local center-regular family.
```

Следующий theorem-facing step therefore должен быть уже не raw local
completeness theorem against `A_reg^loc`, а либо global-to-local trace theorem
for `A_ls`, либо intrinsic characterization theorem showing how the same local
trace is selected inside `A_reg^loc`.
### 1.10.10. C3f: какой trace/germ object реально задаёт `J_0(A_ls)`

После C3e следующий вопрос уже не о том, что такое selected family `A_ls`, а о
том, что именно project должен понимать под local trace / germ map `J_0`.

На current repository boundary нужно различать по крайней мере три candidate
readings:

1. `J_amp(c) = C_amp c` — только две leading amplitudes;
2. `J_0(c) = C_center c = [C_amp c; C_reg c]` — полный finite leading-center
   jet, уже реально encoded in the clean code;
3. some higher-order local germ/jet extractor — пока not canonical, because the
   full intrinsic local selected family is still open.

Лучший theorem-facing choice сейчас есть именно second option:

```text
J_0(c) := C_center c.
```

Причина в том, что этот object ещё остаётся exact on the current repository
boundary, но уже distinguishes raw center data from the selected regularity-zero
slice. `J_amp` становится эквивалентным только после restriction to `A_ls`, а
higher-order germ extractor пока не имеет canonical live-code definition.

### Почему `J_0 = C_center` является exact current trace map

По live code `make_center_constraint_matrix(...)` и `TrialSpace.basis_eval(...)`
trace map `C_center` строится из значений trial basis at `x = x0`, divided by
`x0^n` or `x0^(n-1)` for the relevant channels. Так как basis functions имеют
вид

```text
x^p * t^k,   t = (x - x0)/(1 - x0),
```

то при `x = x0` все columns with `k > 0` vanish exactly. Поэтому `C_center`
вообще не видит higher center coefficients current trial ansatz. Он видит только
четыре `k = 0` columns of

```text
u_s, u_n, varphi, psi.
```

На этих columns получается exact block

```text
[ 1      0      0      0 ]
[ 0      0      1      0 ]
[ 0      1    lambda_c/n  0 ]
[ 0      0    -lambda_c   1 ]
```

с determinant `-1`. Значит, `J_0 = C_center` — это exact rank-4 finite
leading-center-jet extractor current weighted ansatz, а не просто heuristic
small-`x` probe.

Что `J_0` forgets:

- все higher `k >= 1` local center coefficients;
- все channels вне этого leading center jet;
- any intrinsic higher-order local selected-germ structure.

То есть `J_0` — это finite leading-center trace, но не full local formal germ.

### Exact selected trace theorem at the current weighted-ansatz boundary

Для current selected family

```text
A_ls = im(P_sel D_amp),
P_sel = H^(-1) C_center^T (C_center H^(-1) C_center^T)^(-1),
D_amp = [[I_2], [0]],
```

имеем exact identity

```text
J_0(A_ls) = C_center(im(P_sel D_amp)) = im(D_amp).
```

Итак, selected local trace object now reads exactly as the 2D plane

```text
A_sel,trace^loc = J_0(A_ls) = im(D_amp)
```

inside the 4D center-data space.

Moreover,

```text
J_0|_{A_ls} : A_ls -> im(D_amp)
```

is bijective, with inverse given by the selected lift `P_sel` on that plane:

```text
c in A_ls  <->  c = P_sel J_0(c),
J_0(c) in im(D_amp).
```

Отсюда сразу следует coordinate-independence: если заменить basis of `A_ls` на
`M T` with invertible `T`, image plane `J_0(A_ls)` не меняется, меняются только
coordinates inside the same 2D selected plane.

### Relation to previously studied local objects

Этот trace reading exactly matches the already studied leading local data:

- first two coordinates of `J_0` are the same leading amplitudes `(A_us, A_phi)`
  that earlier center analysis tracked explicitly;
- the last two coordinates are the leading regularity-defect rows whose
  vanishing gave the earlier two-parameter leading regular family condition;
- therefore `J_0(A_ls)` is much narrower than the previously too-broad raw local
  object `A_reg^loc`.

But `J_0(A_ls)` still lives only at the finite leading-center-jet layer. It does
not yet identify a full intrinsic higher-order local selected family.

### Conservative C3f conclusion

C3f closes the following statement at the current weighted-ansatz boundary:

1. best current theorem-facing meaning of `J_0` is the exact finite leading-
   center jet map `J_0 = C_center`;
2. the selected trace object is exactly
   `J_0(A_ls) = im(D_amp)`, a basis-independent 2D plane;
3. `J_0|_{A_ls}` is bijective, with inverse selected lift `P_sel`;
4. higher-order intrinsic local-germ selection is still open.

Следовательно, следующий comparison stage уже разумно формулировать first
against this selected leading-center trace plane `J_0(A_ls)`, а не against the
full unrestricted local center-regular family.
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


### 1.10.11. C3g: recovering `im(D_amp)` on the continuum/local side

After C3f the next theorem-facing question is no longer a full intrinsic
higher-order local selector. At this step the target is narrower: can the
current continuum/local side already recover the same selected leading-center
trace plane that is closed on the weighted-ansatz boundary as

```text
J_0(A_ls) = im(D_amp).
```

#### Which local object should now be compared

The best current theorem-facing local candidate here is not a full higher-order
selected germ family. It is only the selected leading-center trace object,
written in the same coordinates as the exact current trace map

```text
J_0 = C_center.
```

So one should compare not an arbitrary quadruple `(U0, N0, P0, Y0)`, but the
trace vector

```text
tau(U0, N0, P0, Y0)
  = [U0, P0, N0 + (lambda_c / n) P0, Y0 - lambda_c P0].
```

This is the smallest current continuum/local object that is directly comparable
with the already closed global selected trace plane `im(D_amp)`.

#### Why the current `J_0` coordinates are fixed this way

The updated `formal_local_family_check.py` now makes explicit a structural fact
of the live clean background path itself.

On the active clean boundary the imposed background BCs are

```text
T_sn(x0) = 0,
u_r(x0) = 0,
varphi(x0) = 0,
```

and in the live clean background

```text
lambda_theta0 = r_0 / x.
```

Therefore, on the current truncated clean boundary,

```text
lambda_theta0(x0) = r_0(x0) / x0 = 1
```

exactly, because `u_r(x0) = 0` means `r_0(x0) = x0`.
Representative live clean checks at `q = 11.1, 17.3, 17.6, 17.8` MPa confirm
that the current path indeed gives

```text
u_r(x0) = 0,
T_sn(x0) = 0,
varphi(x0) = 0,
lambda_theta0(x0) = 1,
lambda_s0(x0) > 1.
```

So the theorem-facing local comparison with `J_0(A_ls)` must preserve exactly
this same `x0`-trace convention. If one silently changes the fourth coordinate,
one is already comparing with another local trace object.

#### Symbolic recovery of `im(D_amp)` from the local leading block

At the singular leading-center level the clean mixed equations give

```text
E_un     = n N0 + lambda_c P0 = 0,
E_gtheta = n N0 + Y0 = 0.
```

Hence

```text
N0 = -(lambda_c / n) P0,
Y0 = lambda_c P0.
```

Substituting into the current theorem-facing trace coordinates gives

```text
tau(U0, N0, P0, Y0) = [U0, P0, 0, 0] = D_amp [U0, P0].
```

Therefore, at the current leading-center-jet level, the selected
continuum/local trace plane agrees exactly with the global selected trace plane:

```text
A_sel,lead-trace^loc = im(D_amp).
```

This is already an exact symbolic identity at the selected leading-center-trace
level.

#### Why the older richer local object is not a direct contradiction

The same helper now also checks the coordinate sensitivity explicitly.
If one keeps the same first three coordinates but replaces the fourth by

```text
Y0 - P0,
```

then after the same singular substitution one gets

```text
[U0, P0, 0, (lambda_c - 1) P0].
```

So equality with `im(D_amp)` then fails generically unless `lambda_c = 1`.
Therefore the older richer local object written through `Y0 = P0` does not yet
give a direct contradiction to the selected trace theorem. It corresponds to
another local trace normalization, and that normalization has not yet been
reconciled with the current exact `J_0 = C_center` coordinates.

#### Conservative C3g conclusion

C3g closes exactly the following statement.

1. The correct theorem-facing local comparison object for the selected trace
   stage is the selected leading-center trace written in the same coordinates
   as `J_0 = C_center`.
2. In these coordinates the singular local compatibility block recovers exactly
   the selected trace plane `im(D_amp)`.
3. This is **not** a proof of a full intrinsic higher-order local selector.
4. The exact remaining gap is now a higher-order intrinsic selected-family
   theorem, or an explicit reconciliation theorem between the current `J_0`
   coordinates and any alternative richer-local trace normalization.


### 1.10.12. C3h: reconciling richer local trace charts with `J_0 = C_center`

After C3g the next theorem-facing question is no longer whether the leading
selected trace plane is `im(D_amp)`. That part is already closed in current
`J_0` coordinates.

The exact C3h target is to reconcile this canonical leading trace with the
richer local trace objects suggested by the regular-singular expansions.

#### Best current richer trace candidate

The best current richer theorem-facing object is the first truncated
regular-singular jet

```text
Xi_rich^(1,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1],
```

with

```text
Delta_un^(0)      = N0 + (lambda_c / n) P0,
Delta_psi,eta^(0) = Y0 - eta P0.
```

This object extends `J_0` by one post-leading layer and keeps the
fourth-coordinate normalization explicit. It is not yet canonical because it
depends both on the chosen parameter `eta` and on how many higher coefficients
are retained.

#### Canonical projection to the current selected trace

For every such richer trace chart there is an exact triangular projection

```text
Pi_eta_to_J0 : Xi_rich^(1,eta) -> J_0,
```

given by

```text
[U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1]
  |->
[U0, P0, Delta_un^(0), Delta_psi,eta^(0) + (eta - lambda_c) P0].
```

This is just the identity

```text
Y0 - lambda_c P0 = (Y0 - eta P0) + (eta - lambda_c) P0.
```

So the fourth defect coordinate by itself is not canonical, but its projection
back to current `J_0` coordinates is canonical.

#### The selected object inside the richer trace

Using the current live local selected relations

```text
N0 = -(lambda_c / n) P0,
Y0 = lambda_c P0,
```

the selected richer trace is not generally the zero-defect slice. Instead it is
the 2D lifted plane

```text
im(D_rich,eta),

D_rich,eta =
[[1, 0],
 [0, 1],
 [0, 0],
 [0, lambda_c - eta],
 [0, 0],
 [0, 0],
 [0, 0],
 [0, 0]].
```

The exact checked reconciliation identity is

```text
Pi_eta_to_J0(im(D_rich,eta)) = im(D_amp).
```

Hence the invariant core that should be preserved at higher order is not
"zero fourth defect in every richer chart". It is the 2D lifted selected object
whose canonical `J_0` projection equals `im(D_amp)`.

#### Special case `eta = 1`

The older richer local note corresponds to `eta = 1`.
Then the selected richer trace carries the lifted fourth component

```text
(lambda_c - 1) P0,
```

which is nonzero on the representative active clean points because
`lambda_c = lambda_s0(x0)` is slightly above `1` there.
So the older richer local trace was not a direct contradiction to the selected
trace theorem; it was simply another trace normalization chart.

#### Conservative C3h conclusion

C3h closes exactly the following statement.

1. The best current richer local trace object is a truncated regular-singular
   jet with explicit normalization parameter `eta`.
2. There is an explicit projection `Pi_eta_to_J0` from that richer trace chart
   to the canonical selected trace coordinates.
3. The invariant selected object to preserve at higher order is a 2D lifted
   plane in the richer trace space whose `J_0` projection is exactly
   `im(D_amp)`.
4. This is still not a full higher-order selected-family theorem.


### 1.10.13. C3i: first higher-order preservation for the lifted selected family

After C3h the correct question is no longer whether the raw 2D lifted plane
`im(D_rich,eta)` survives unchanged. The first checked post-leading recurrence
shows that the preserved object is slightly larger.

#### First checked post-leading recurrence

In the richer trace chart

```text
Xi_rich^(1,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1],
```

the first post-leading recurrence is exactly independent of the already selected
leading amplitudes `(U0, P0)`: the Jacobian of the checked first post-leading
rows with respect to `(U0, P0)` is identically zero.

At this layer the flexural block is still rigid under nonresonance:

```text
N1 = P1 = Y1 = M1 = Q0c = 0.
```

But the membrane block leaves one free parameter `T1`, with

```text
U1 = alpha * T1,
V1 = beta  * T1,

alpha = (-n*nu - n - 2*nu + 2)/(-n^2 + n + 2),
beta  = (n*nu + n + 4)/(-n^2 + n + 2).
```

For `n > 2` and positive `nu` the zero loci of `alpha` and `beta` lie outside
that regime, so this membrane nullmode is visible already in the current richer
jet.

#### Consequence for the selected lifted object

The raw lifted selected plane from C3h,

```text
im(D_rich,eta),
```

fixes `U1 = N1 = P1 = Y1 = 0`, so it is too small for the first checked
post-leading recurrence. Therefore it is **not** exactly preserved.

The smallest corrected object visible in the current richer jet is the 3D plane

```text
Xi_sel,corr^(1,eta)
  = {[U0, P0, 0, (lambda_c - eta) P0, U1, 0, 0, 0]}
  = im(D_rich,eta^corr),
```

with

```text
D_rich,eta^corr =
[[1, 0, 0],
 [0, 1, 0],
 [0, 0, 0],
 [0, lambda_c - eta, 0],
 [0, 0, 1],
 [0, 0, 0],
 [0, 0, 0],
 [0, 0, 0]].
```

If one wants a coefficient-faithful object that keeps the hidden membrane
parameter explicit, one should enlarge the jet to

```text
Xi_rich^(1+,eta)
  = [U0, P0, Delta_un^(0), Delta_psi,eta^(0), U1, N1, P1, Y1, V1, T1],
```

and use the exact 3D plane spanned by the two leading selected amplitudes and
by the membrane nullmode `(U1, V1, T1) = T1 * (alpha, beta, 1)`.

#### Canonical trace is still preserved

The crucial invariant stays the same:

```text
Pi_eta_to_J0(im(D_rich,eta^corr)) = im(D_amp),
Pi_eta_to_J0(im(D_rich,eta^aug))  = im(D_amp).
```

So the first checked higher-order correction does not destroy the already closed
selected leading-center trace plane. It only thickens the richer lift above it
by one membrane direction.

#### Checked next support and conservative conclusion

Within the same frozen-principal recurrence model, once this membrane thickening
is admitted, the next checked layer closes uniquely to zero under the same
nonresonance assumptions. Thus the current verified statement is:

1. raw `im(D_rich,eta)` is not exactly preserved at the first checked
   post-leading order;
2. a corrected one-parameter membrane thickening is preserved instead;
3. its canonical `J_0` projection remains exactly `im(D_amp)`;
4. this is still not an all-orders intrinsic higher-order selected-family
   theorem.


### 1.10.14. C3j: canonical treatment of the membrane thickening direction

After C3i the main question is no longer whether a raw 2D lifted family is
preserved. The correct question is what the extra membrane direction means
canonically.

#### Kernel structure of the corrected higher-order family

The corrected higher-order selected family from C3i is 3D. In the visible richer
jet it is

```text
Xi_sel,corr^(1,eta) = im(D_rich,eta^corr),
```

and in the coefficient-faithful augmented jet it is

```text
Xi_sel,corr^(1+,eta) = im(D_rich,eta^aug).
```

For both objects the canonical projection back to `J_0` acts on the coefficient
space as

```text
(a, b, s) |-> [a, b, 0, 0],
```

so its kernel is exactly one-dimensional. In the visible chart it is the pure
`U1` direction; in the augmented chart it is the membrane nullmode

```text
g_mem^aug = [0, 0, 0, 0, alpha, 0, 0, 0, beta, 1].
```

The next checked recurrence layer still does not kill this kernel direction.
So the membrane thickening line survives all currently checked local tests.

#### No canonical 2D section from the checked local data

The checked local data do not yet provide a canonical normalization that removes
this line. The reason is exact: there is a whole family of 2D sections of the
corrected 3D family, namely the graphs of arbitrary linear maps from the two
selected quotient coordinates into the membrane parameter. On the coefficient
space this family is

```text
S_(ell1,ell2) =
[[1, 0],
 [0, 1],
 [ell1, ell2]].
```

For every choice of `(ell1, ell2)` one has

```text
Pi_eta_to_J0(D_rich,eta^corr S_(ell1,ell2)) = D_amp,
```

and similarly in the augmented chart.
Thus the current recurrence and trace data do not select one preferred 2D
section. Conditions like `U1 = 0` are section choices, not yet canonical
higher-order normalizations.

#### Conservative theorem-facing reading

At the checked order the membrane thickening direction should therefore be read
as quotient-like.
This is stronger than merely saying ?open?, because the canonical quotient object
is now clear; and it is weaker than claiming a proved gauge symmetry.

The best current theorem-facing local object is

```text
im(D_rich,eta^corr) / span(g_mem),
```

or equivalently its augmented version

```text
im(D_rich,eta^aug) / span(g_mem^aug).
```

This quotient is canonically identified by the `J_0` projection with the already
closed selected leading-center trace plane `im(D_amp)`.

#### Conservative C3j conclusion

The checked local theory now supports the following statement.

1. The membrane thickening direction is not canonically removed by the current
   checked local recurrence data.
2. The correct current theorem-facing local object is the quotient class of the
   corrected 3D higher-order selected family modulo that membrane direction.
3. This quotient still carries exactly the same canonical selected leading trace
   plane `im(D_amp)`.
4. The next open question is whether a later intrinsic higher-order rule picks a
   distinguished representative of this quotient or whether the quotient itself
   is the final local selected object.


### 1.10.15. C3k: no intrinsic canonical representative is yet justified beyond the membrane quotient

After C3j the local selected object at the checked higher-order level was the
quotient

```text
im(D_rich,eta^corr) / span(g_mem),
```

because the corrected 3D family carried an exact one-dimensional membrane kernel
of the canonical `J_0` projection. The next question is whether the checked
local equations already contain an intrinsic rule that picks one distinguished
representative from each quotient class.

The current checked local boundary does not support such a rule.

First, the next checked local compatibility layer does not distinguish
representatives inside the membrane-thickened corrected family. Second, the
checked residual is already exactly zero along that membrane direction inside
the coefficient-faithful corrected family, so checked local residual
minimization also does not select a unique representative. Third, chart
conditions such as `U1 = 0` are not intrinsic: after a quotient-preserving chart
change they become arbitrary 2D sections of the same corrected 3D family.
Finally, orthogonality or minimal-norm rules do produce a unique section once an
SPD metric is chosen, but the resulting section depends on that metric. On the
current local boundary no intrinsic local metric has been derived that would
canonically reproduce one representative per quotient class.

So at the present checked level the strongest theorem-facing statement is not a
canonical 2D normalization theorem. It is the strengthened quotient theorem:
all currently justified local selected invariants factor through the membrane
quotient, and all representatives of one quotient class have the same canonical
selected leading-center trace plane `im(D_amp)`.

Therefore the best current local selected object remains the quotient itself,
not a canonically normalized representative. What remains open is whether a
later intrinsic higher-order selector exists, or whether this quotient is
already the final theorem-facing local selected object.


### 1.10.16. C3l: on the current checked local boundary the quotient object is final

C3l is the controlled stop-rule decision for the current local fork.
After C3j/C3k the remaining alternatives were:

1. derive an intrinsic higher-order selector that canonically chooses one
   representative of each membrane-quotient class;
2. justify that the quotient itself is already the final local theorem-facing
   object on the current checked boundary;
3. leave the fork unresolved.

On the current checked boundary the second alternative is the strongest
responsible conclusion.

The reason is now twofold.
First, none of the strongest plausible intrinsic selectors survives checking:
next checked local compatibility does not distinguish representatives, checked
local residual minimization does not distinguish them either, chart conditions
such as `U1 = 0` are only section choices, and orthogonality / minimal-norm
rules require an extra metric choice. Second, every currently justified local
selected invariant factors through the membrane quotient. The canonical `J_0`
trace on the corrected 3D family is exactly `D_amp` composed with the quotient
map `(a, b, s) -> (a, b)`, the checked residual vanishes identically on the
corrected family, and the next checked local compatibility layer contributes no
representative-level invariant on this boundary.

Therefore on the current checked local boundary the correct theorem-facing local
selected object is the quotient

```text
im(D_rich,eta^corr) / span(g_mem),
```

or equivalently its coefficient-faithful augmented version. This is a
boundary-scoped finality statement: it does not exclude the possibility that a
future unchecked higher-order intrinsic selector could appear outside the
current checked boundary. It does mean that, within the currently checked local
theory, canonical comparison to the global selected family must proceed through
this quotient object.

