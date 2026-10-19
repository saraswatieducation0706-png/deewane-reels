# GATE ME 2027 Test Series - topic register
# (subject_code, subject_name, [ (topic_test_id, topic_test_title, [(topic, imp), ...]), ... ])
# imp: A = top weightage / asked almost every year, B = regular, C = occasional
SUBJECTS = [
("GA", "General Aptitude", [
  ("GA1", "Verbal Aptitude", [
    ("Grammar, articles, tenses, subject-verb agreement", "A"),
    ("Vocabulary: words, idioms, phrases in context", "A"),
    ("Reading comprehension & inference", "A"),
    ("Sentence ordering / completion, critical reasoning", "B"),
    ("Narrative sequencing", "C")]),
  ("GA2", "Quantitative Aptitude", [
    ("Percentages, ratio & proportion, averages", "A"),
    ("Time-speed-distance, time & work", "A"),
    ("Data interpretation (tables, bar & pie charts)", "A"),
    ("Number system, powers, logarithms, series", "B"),
    ("Permutations, combinations & basic probability", "B"),
    ("Mensuration & elementary statistics", "B")]),
  ("GA3", "Analytical & Spatial Aptitude", [
    ("Logical deduction & syllogisms", "A"),
    ("Arrangement, ordering & grouping puzzles", "A"),
    ("Spatial: folding, cutting, rotation, mirror images", "A"),
    ("Patterns in 2D/3D figures, counting figures", "B"),
    ("Direction sense, blood relations, coding", "C")]),
]),
("EM", "Engineering Mathematics", [
  ("EM1", "Linear Algebra", [
    ("Matrix algebra, rank, determinants", "A"),
    ("Systems of linear equations, consistency", "A"),
    ("Eigenvalues & eigenvectors, Cayley-Hamilton", "A"),
    ("Special matrices (symmetric, orthogonal), diagonalisation", "B")]),
  ("EM2", "Calculus & Vector Calculus", [
    ("Limits, continuity, mean value theorems", "B"),
    ("Maxima-minima (single & multivariable), Taylor series", "A"),
    ("Definite & improper integrals, area/volume", "A"),
    ("Partial derivatives, double & triple integrals", "B"),
    ("Gradient, divergence, curl; line & surface integrals", "A"),
    ("Gauss, Stokes & Green theorems", "B")]),
  ("EM3", "Differential Equations & Complex Variables", [
    ("First-order ODEs (separable, exact, linear)", "A"),
    ("Higher-order linear ODEs with constant coefficients", "A"),
    ("Cauchy-Euler equation, initial & boundary value problems", "B"),
    ("Laplace transforms", "B"),
    ("PDEs: heat, wave, Laplace equations, separation of variables", "B"),
    ("Analytic functions, Cauchy-Riemann, Cauchy integral, residues", "B"),
    ("Taylor & Laurent series (complex)", "C")]),
  ("EM4", "Probability, Statistics & Numerical Methods", [
    ("Probability, conditional probability, Bayes theorem", "A"),
    ("Random variables; binomial, Poisson, normal, exponential distributions", "A"),
    ("Mean, median, mode, standard deviation, correlation & regression", "B"),
    ("Numerical solution of equations (Newton-Raphson, bisection)", "A"),
    ("Numerical integration (trapezoidal, Simpson)", "A"),
    ("Numerical solution of ODEs (Euler, RK)", "B")]),
]),
("MEC", "Engineering Mechanics", [
  ("MEC1", "Statics", [
    ("Free-body diagrams & equilibrium", "A"),
    ("Plane trusses (joints & sections), zero-force members", "A"),
    ("Friction: dry friction, wedges, belt/rope friction", "A"),
    ("Virtual work", "B"),
    ("Centroid & moment of inertia", "B")]),
  ("MEC2", "Dynamics", [
    ("Kinematics of particles & rigid bodies in plane motion", "A"),
    ("Newton's laws, D'Alembert, dynamics of rigid bodies", "A"),
    ("Work-energy principle", "A"),
    ("Impulse-momentum (linear & angular)", "B"),
    ("Impact & coefficient of restitution", "B")]),
]),
("SOM", "Strength of Materials", [
  ("SOM1", "Stress, Strain & Failure Theories", [
    ("Stress-strain, elastic constants, Poisson's ratio", "A"),
    ("Mohr's circle for plane stress & plane strain", "A"),
    ("Thermal stresses & compound bars", "A"),
    ("Theories of failure", "B"),
    ("Strain gauges & rosettes", "C"),
    ("Testing: tensile, hardness, impact", "C")]),
  ("SOM2", "SFD, BMD & Stresses in Beams", [
    ("Shear force & bending moment diagrams", "A"),
    ("Bending stresses in beams", "A"),
    ("Shear stress distribution in beams", "A"),
    ("Composite/flitched beams", "C")]),
  ("SOM3", "Deflection, Energy Methods & Columns", [
    ("Deflection of beams (double integration, Macaulay)", "A"),
    ("Moment-area & superposition", "B"),
    ("Strain energy & Castigliano's theorem", "B"),
    ("Euler buckling of columns, end conditions", "A")]),
  ("SOM4", "Torsion, Pressure Vessels & Combined Loading", [
    ("Torsion of circular shafts (solid, hollow, stepped)", "A"),
    ("Thin cylinders & spheres", "A"),
    ("Combined bending, torsion & axial loading", "B"),
    ("Close-coiled helical springs (as SOM)", "C")]),
]),
("TOM", "Theory of Machines & Vibrations", [
  ("TOM1", "Kinematics of Mechanisms", [
    ("Mobility (Grubler), kinematic chains & inversions", "A"),
    ("Velocity analysis, instantaneous centres", "A"),
    ("Acceleration analysis, Coriolis component", "B"),
    ("Slider-crank kinematics & dynamics", "A")]),
  ("TOM2", "Gears, Flywheels, Governors, Balancing, Gyroscope", [
    ("Gear terminology, interference, contact ratio", "B"),
    ("Simple, compound & epicyclic gear trains", "A"),
    ("Flywheel: turning moment, fluctuation of energy & speed", "A"),
    ("Governors", "C"),
    ("Balancing of rotating & reciprocating masses", "B"),
    ("Gyroscopic couple & effects", "B")]),
  ("TOM3", "Vibrations", [
    ("Free undamped SDOF, natural frequency (energy/equilibrium)", "A"),
    ("Damped free vibration, logarithmic decrement", "A"),
    ("Forced vibration, resonance, magnification factor", "A"),
    ("Vibration isolation & transmissibility", "B"),
    ("Critical speed of shafts (whirling)", "B")]),
]),
("MD", "Machine Design", [
  ("MD1", "Static & Fatigue Design, Shafts", [
    ("Design for static loading, failure theories in design", "A"),
    ("Fatigue: S-N curve, endurance limit, modifying factors", "A"),
    ("Goodman, Soderberg, Gerber criteria", "A"),
    ("Stress concentration & notch sensitivity", "B"),
    ("Shaft design under combined loading", "B")]),
  ("MD2", "Joints, Gears, Bearings, Brakes, Clutches & Springs", [
    ("Bolted, riveted & welded joints (incl. eccentric)", "A"),
    ("Spur & helical gear design (Lewis, wear)", "B"),
    ("Rolling-contact bearings: life & load", "A"),
    ("Sliding (journal) bearings, Petroff", "C"),
    ("Brakes & clutches (uniform pressure/wear)", "A"),
    ("Helical springs design", "B")]),
]),
("FM", "Fluid Mechanics", [
  ("FM1", "Fluid Properties & Fluid Statics", [
    ("Fluid properties: viscosity, surface tension, capillarity", "B"),
    ("Pressure, manometry", "A"),
    ("Hydrostatic forces on plane & curved surfaces", "A"),
    ("Buoyancy & stability (metacentre)", "B")]),
  ("FM2", "Kinematics, Bernoulli & Control-Volume Analysis", [
    ("Fluid kinematics: stream function, potential, vorticity", "A"),
    ("Continuity, Bernoulli equation & applications", "A"),
    ("Control-volume momentum (forces on bends, jets)", "A"),
    ("Flow measurement: venturi, orifice, pitot", "B")]),
  ("FM3", "Viscous & Pipe Flow", [
    ("Laminar flow: Hagen-Poiseuille, Couette", "A"),
    ("Turbulent pipe flow, friction factor, Moody", "B"),
    ("Major & minor losses, pipes in series/parallel", "A"),
    ("Navier-Stokes exact solutions", "B")]),
  ("FM4", "Boundary Layer & Dimensional Analysis", [
    ("Boundary layer: thicknesses, momentum integral", "A"),
    ("Drag & lift basics", "C"),
    ("Dimensional analysis, Buckingham pi", "B"),
    ("Similitude & model studies", "B")]),
]),
("HT", "Heat Transfer", [
  ("HT1", "Conduction & Fins", [
    ("1-D steady conduction, thermal resistance networks", "A"),
    ("Critical radius of insulation", "B"),
    ("Heat generation in solids", "B"),
    ("Fins: efficiency & effectiveness", "A"),
    ("Unsteady conduction: lumped capacitance, Biot number", "A")]),
  ("HT2", "Convection, Radiation & Heat Exchangers", [
    ("Forced convection, dimensionless numbers, correlations", "A"),
    ("Free convection", "C"),
    ("Radiation: black/grey bodies, view factors, radiation networks", "A"),
    ("Heat exchangers: LMTD method", "A"),
    ("Heat exchangers: effectiveness-NTU method", "A")]),
]),
("TD", "Thermodynamics", [
  ("TD1", "First Law & Properties", [
    ("Systems, work & heat, zeroth law", "B"),
    ("First law for closed systems", "A"),
    ("First law for open systems (SFEE)", "A"),
    ("Pure substances, steam tables, Mollier chart", "A")]),
  ("TD2", "Second Law, Entropy & Exergy", [
    ("Second law, heat engines, refrigerators, Carnot", "A"),
    ("Entropy, entropy generation", "A"),
    ("Availability (exergy) & irreversibility", "A"),
    ("Clausius inequality", "C")]),
  ("TD3", "Thermodynamic Relations & Gas Mixtures", [
    ("Ideal & real gases, compressibility", "B"),
    ("Maxwell relations, Clapeyron, Tds equations", "B"),
    ("Ideal gas mixtures", "C"),
    ("Processes of ideal gases (polytropic, isentropic)", "A")]),
]),
("APP", "Thermal Applications", [
  ("APP1", "Power Cycles & Compressors", [
    ("Rankine cycle, reheat & regeneration", "A"),
    ("Brayton cycle, regeneration, intercooling", "A"),
    ("Reciprocating air compressors, volumetric efficiency", "B")]),
  ("APP2", "IC Engines, Refrigeration & Air-conditioning", [
    ("Otto, Diesel & dual cycles", "A"),
    ("Engine performance parameters", "B"),
    ("Vapour-compression refrigeration (incl. modifications)", "A"),
    ("Gas & vapour-absorption refrigeration", "C"),
    ("Psychrometry & air-conditioning processes", "A")]),
  ("APP3", "Turbomachinery", [
    ("Velocity triangles, Euler turbine equation", "A"),
    ("Impulse & reaction steam turbines", "B"),
    ("Pelton, Francis & Kaplan turbines", "A"),
    ("Centrifugal pumps, specific speed, NPSH", "A")]),
]),
("MAT", "Engineering Materials", [
  ("MAT1", "Engineering Materials", [
    ("Crystal structures, defects", "B"),
    ("Phase diagrams, iron-carbon diagram, lever rule", "A"),
    ("Heat treatment (annealing, normalising, hardening, tempering)", "A"),
    ("Stress-strain behaviour of engineering materials", "B"),
    ("Strengthening mechanisms", "C")]),
]),
("MFG", "Manufacturing & Metrology", [
  ("MFG1", "Casting", [
    ("Patterns & allowances, moulding sands", "B"),
    ("Gating design: filling time, Bernoulli", "A"),
    ("Riser design: Chvorinov's rule, modulus", "A"),
    ("Solidification & casting defects", "C")]),
  ("MFG2", "Metal Forming", [
    ("Plastic deformation, hot & cold working", "B"),
    ("Rolling: draft, bite angle, roll force", "A"),
    ("Forging, extrusion & wire drawing loads", "A"),
    ("Sheet metal: blanking, punching, deep drawing", "A")]),
  ("MFG3", "Joining & Powder Metallurgy", [
    ("Arc welding: power, heat input, arc characteristics", "A"),
    ("Resistance, gas & solid-state welding", "B"),
    ("Brazing, soldering, welding defects & HAZ", "C"),
    ("Powder metallurgy fundamentals", "C")]),
  ("MFG4", "Machining Mechanics & Tool Life", [
    ("Merchant's circle, cutting forces, shear angle", "A"),
    ("Tool life (Taylor), economics of machining", "A"),
    ("Machining time: turning, drilling, milling, grinding", "A"),
    ("Tool geometry & materials, chip formation", "B")]),
  ("MFG5", "Non-traditional Machining, Tooling & CIM", [
    ("ECM, EDM, USM, AJM, LBM & EBM", "A"),
    ("Jigs & fixtures, 3-2-1 principle", "B"),
    ("CNC part programming, CAD/CAM, CIM basics", "B"),
    ("Additive manufacturing", "C")]),
  ("MFG6", "Metrology & Inspection", [
    ("Limits, fits & tolerances, GO/NO-GO gauges", "A"),
    ("Linear & angular measurement, slip gauges, sine bar", "A"),
    ("Comparators, interferometry", "B"),
    ("Surface roughness & form measurement", "B")]),
]),
("IE", "Industrial Engineering", [
  ("IE1", "Production Planning & Control", [
    ("Forecasting models (moving average, exponential smoothing)", "A"),
    ("Aggregate planning, MRP", "B"),
    ("Scheduling: Johnson's rule, priority rules", "A"),
    ("Lean manufacturing, line balancing", "C")]),
  ("IE2", "Inventory Control", [
    ("EOQ & deterministic models (incl. production, discounts)", "A"),
    ("Safety stock, reorder point, inventory systems", "B")]),
  ("IE3", "Operations Research", [
    ("Linear programming: graphical & simplex", "A"),
    ("Transportation & assignment problems", "A"),
    ("PERT & CPM", "A"),
    ("Simple queuing models (M/M/1)", "A"),
    ("Network flow models", "C")]),
]),
]

# Questions per subject in each full-length mock (1-mark, 2-mark). Totals: 30 x 1-mark + 35 x 2-mark = 65 Q, 100 marks
MOCK_SLOTS = {
 "GA": (5, 5), "EM": (5, 4),
 "MEC": (1, 2), "SOM": (2, 3), "TOM": (2, 3), "MD": (2, 2), "FM": (2, 3), "HT": (2, 2),
 "TD": (2, 2), "APP": (2, 2), "MAT": (0, 1), "MFG": (4, 4), "IE": (1, 2),
}
