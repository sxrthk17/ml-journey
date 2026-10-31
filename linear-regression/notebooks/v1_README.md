### V1 FINAL README:

For V1, at day 1, we officially started this project of our

in theory I learned: Correlation: what does it mean, how to interpret r and what geometrical relation does two features have on the basis on r, as r = cos($\theta$). Two uncorrelated features can be in relaionship !

then, I learned about confounding, which is a concept where on feature x1 steals the credit of other feature x2, as x1 and x2 sits on the same plane or line, if relation is plotted btw x1 and y, x1 might not be influencing this relationship but it can be x2, but as x1 and x2 sits closely, x1 is getting the credit. To solve this: we can use Crude model, adjusted model and holding constant method. Currently as of Day 8, I have not found any feature which is confounding

then i learnt about simpson's paradox: How accumulated/pooled dataset or feature can have different trend that clustered or hued data. In rentals by hour if we see on the pooled data, we only get two spikes one in morning around 7 to 10 and other in evening 4 to 6 ,but when plotted considering a third variable weekday, when it is weekday meaning from Mon to Fri, when people going to work travel we see two peaks, when people go to their work and when people come from work. But during weekends that is saturday sunday, we see a bump or rise in afternoon hours, when i thnk people rent bikes to have a trip or comute to some place to like chill, or do their side quest and all. So this relation was getting overshadowed by the weekdays in pooled plot. Because pooled plot has more data about weekdays than weekend okay !! 

We performed in depth EDA, like year wise rentals like 2011 vs 2012, then season wise, weather situation wise, the outliers in features and target variable, distirbution on features, scatter plots, time series plot acorss two years of rentals: seeing relative increase in 2012. 
Hourly correlation between temperature and count, 4 variable correlation with `cnt` 

A correlationmatrix across 5 variables, seeing a STRONG CORRELATION between `atemp` and `temp`.

Average season, hr and weather situation wise rental bar plot.
before and after log transformation plot of y-target feature.


After EDA, for data loading created a helper function: `load_csv(path)` that fetches hour.csv, removes instant,casual and registered for  


On day 2: 

we learnt about various mathematical terms: 
Covariance, variance, orthogonality,inner product, dot product, orthogonal relation between e and x, finding slope and intercept for our SLR model.Centered vectors (X - Xmean) 

Residual Sum of Squares and minimising that, therefore the slope becomes Cov(X,y) / Var(X). 
beta_hat(y/x) = Cov(X,y)/Var(X) and
beta_hat(X/y) = Cov(X,y)/var(X) 
B(y/x) . B(x/y) = r² <= 1 unless |r| = 1.

y = beta_0 + X * beta_1, beta_1 is the slope and beta_0 is the intercept.

Linear Regression is Minimising RSS! == Minimising OLS

Day 3: Multiple Linear Regression:

learned and applied design matrix, column space, row space, null space, kernel, Image, orthogonal projection, normal equations, and the hat matrix in multiple linear regression. Hessian Matrix, why y lies outsid X's reachable space? beta is the true slope and beta_hat is the predicted slope value for a particular plane or line.

y = beta_0 + X1 * beta_1 + X2 * beta_2 etc etc, beta_1 is the slope and beta_0 is the intercept.

for MLR we find the beta_hat matrix of coefficients using: (X.T @ X)_inverse @ X.T @ y

here X is design matrix, formed by stacking a column of 1's as first column in X(feature matrix).

for matching the shapes while multiplying with y, we take transpose of X. 

Here we performed our first data transformation, which was standardisation: using `StandardScaler` from sklearn.preprocessing it uses Z = X - mean / std, the Z-score to standardise our data, where mean of the data is 0 and it has a unit standard deviation. We can see why standardisation work by comparing R2 scores and coefficients, test score was improved from 0.09 to 0.14 !!

Day 4: Gradient Descent: a day full of heavy maths, complex wordings and technical definition.

this is the day i realised that i am not changing slope and intercept, I am minimsing RSS or OLS !! The gradient descent is an optimisation technique where we "Step Down" to the local minimum of the Loss Function. This day was crucial as it shaped our brain to think in terms of derivatives, gradients step size and learning rate. 

Thoery we learnt: Gradient descent, eigenvectors and eigenvalues and constructing hessian matrix from XTX and then finding eigenvalues and eigenvectors of Hessian Matrix. We learnt about unit vectors, identity matrix, matrix transpose ((A.B)T = B.T @ A.T). Limits and partial derivatives, along with gradient vector. A gradient is pointing uphill but when we negate it it points downhill to steepest local minimum.

max_eigenvalue = steepness of canyon walls of loss parabola

min_eigenvalue = flatness of valley floor, if valley floor is flat, our condition number becomes infinitely larger. As condition number k = max_eigenvector/min_eigenvector.

The loss function can be of two type:
1. Circular Bowl: Well conditioned: When all features are on the same scale are are completely uncorrelated. (symmetric bowl)

2. Stretched bowl: Narrow Canyon ill condition: When features are on vastly different scales and strongly correlated. (elongated narrow eliptical canyon)
convergence means finding the optimal value, high k == slow convergence. Step Size = Slope * Learning Rate and then New intercept = Old_intercept - Step Size. repeat this for n epochs. Two or more derivative of a function are called gradients, as we use the gradient to find step size and descend down to the lowest point, that is GRADIENT DESCENT !! Hessian tells uus how "fast" the slope is changing, the curvatureof loss surface in every direction.

We made a custom gradient descent function, optimised it multiple time, kept track of loss histroy, potted it against epochs, saw big and baby step in action. kept lr = 1/max_eigenvector if nothing is specified and if lr is above 2/max_eigenvecctor we raised a warning that lr is above or at the stabitlity limit, except covergence. everytime we predict using last slope and intercept, then we find the gradient for that beta, update the beta and step down, we have a tolerance meaning if diff btw last two step size < tolerance then stop !


Day 5: This was even more intresting, we saw SGD in action. As full batch GD requires computing gradients across n data points so we get o(ND) complexity. To fix that we have something known as mini batch and stochiastic gradient descent. Here we learnt about batch size, bias, variance, OLS: estimation technique to fing the least Sum of squares. Estimator vs Estimate, Consistency Efficiency, i.i.d: Independent, and identically distributed features. 

we slice the path --> predict --> get residual --> gradient --> update. 
Learned about learning rate decay and decay type (time and exponential) Cooked even harder there, wrote from scratch and performed multiple variant evaluation: check out the notebook for that. 

predict --> see loss --> then calc gradient update beta and repeat from start to end ndexof a batch size. 
added new parameter stop_reason; divergence, tolerance/convergence and max_epochs.

Compared with our Normal Equation MLR !! Got same results !! Then calculated band fucntion which is loss histroy - cfloss, mean of loss in closed form. Used 7 to 9 type of different variant combinations !!

Day 6- Maximum likelihood estimation !!

DOne with theory, practical for buffer day now !

Day 7- Best and intresting of them all:
Residual Analysis and Regression Diagnostics.

Made different helping metrices function from mathematical formulas, MAE, RMSE R2, ADJ_r2, MSE, SSE, SST, MSS/ESS. Got to know what are they how they are interpreted.

Diagnostics: fitted vs residual scatterplot, then qq plot of residuals to see if they are normally distributed, Heterodasciticity and mean error trend plot, saw how heterodecaticity changes the residual values asour data was increasing the values were skyrocketing, 

Residual vs fitted for all parameters, Average Residual And Spread by hour of day *** the most important and incredibly insightful plot of the project !!

Learned about rolling average, considered 168 hours : a weeks window size, and rolled over it, at the start it was underpredicting, then it started overpredicting.

Autocorrelation, correlation between residual t and residual t+1. The purple commet plot. 

log transformed y and then plotted everything again, this time the heterodescaticity problem was lower that previous. 

At last checked if my helper functions were producing same as sklearn's !! 



Day 8:
Hypothesis testing, Sampling error, t statistics and distribution, p-value, degree of freedom, confidence interval, efffect size, SE as wobble in slope when data changes.

Different conditions as Higher Noise more SE, More sample size decreases wobble, wider feature smaller SE, High multicollinearity means massive SE, 

Computed covariance matrix of coefficients, the diagonal represents coefficients variance and other element represent covariance C_bk: b is one feature k is another !
We use SSE to compure RSE Residual Standard Error = root(SSE/n-p-1) p are parameters without intercept. 

After this defined helper functions for summary and metrics, then used train_pool to take traiuning and validation dataset ! 

Then comes the special part, transforming features, cylic and one hot encoded `hr`, one hot encoded season and weathersit. you can see eveyrthing in the table given below. learned a lot of new and amazing pandas functions and mathematics !! It was fun on Day 8 !! 

More about day 8

As of now, 30/10/2026 we have decided to keep these many features for our model.
features = `["holiday", "yr", "season", "weathersit", "hr", "atemp", "hum", "windspeed"]`


I am loving the this comfort i am feeling inthis project after almost a year of uncomforatble-ness and anxiety with procrastination! 

Now i will mintain a daily regular ritual of writing a daily til, everyhting was written today so my real emotions i felt on these days are not captured or logged 









