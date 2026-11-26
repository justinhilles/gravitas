# Validation strategy

- Point sources are tested against inverse square scaling, potential and superposition. Ring gravity is checked against distributed point masses. Disk acceleration is checked against numerical radial integration and the derivative of the potential.
- GRV-0001 compares the central magnetic vector to the ideal Helmholtz-pair field driven in quadrature at each sampled time. Pair rest masses give zero net gravity at the symmetric center. The vector residual and null use a 1e-15 absolute floor in their respective SI units.
- GRV-0002 compares axial acceleration to the closed form using surface density and checks inverse scaling of required mass. A separate unit test uses midpoint integration of 4,000 rings with relative tolerance 1e-7.
- Per-source raw coil fields and ring-mass gravity compare 32- and 64-element quadratures. Field sensitivity is scaled by the individual loop center strength. Ring gravity uses potential divided by a characteristic length as its field scale. Gradient differences compare centered steps of 0.1 and 0.2 mm against a scale from the local gradient or characteristic field over radius. These are convergence gates and do not quantify model-form uncertainty.
- Benchmark relative tolerance is 1e-5 unless a check uses the absolute floor. Schema tests reject mismatched units, invalid orientations, improper safety limits and out-of-domain geometry. Workflow tests exercise seeded replay, recording rejections, SQLite persistence and report export.

The sources-off null removes all modeled sources. It distinguishes the implementation baseline from active observations. A current-off laboratory control would retain coil rest masses and would require its own configuration.
