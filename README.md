**Introduction**

In
this PAF project (Projet d’Application Finale à Télécom ParisTech), our goal is
to implement Artificial Neural Networks in order to detect changes in
time-series. Our dataset is made of measures of RTT in Internet networks.

The first two methods that we used to detect changes
were a simplified version of CUSUM (cumulative sum) and an implementation of
the Bayesian method. Our goal was to see if it was possible to have better results
with neural networks.

As we read a bit about neural networks, we discovered
that our main problem with the simplest kind of neural network (perceptron) was
going to be their absence of memory. They cannot remember what were the
previous outputs which makes things harder when dealing with sequential data. Hopefully,
Tensorflow offers an easy way of implementing LSTM (long short term memory)
neural networks, that take their outputs also as inputs (see [http://colah.github.io/posts/2015-08-Understanding-LSTMs/](http://colah.github.io/posts/2015-08-Understanding-LSTMs/))
– while avoiding the vanishing gradient issue – and allow to work on sequential
data.

**MAP**

[https://github.com/Albertobegue/PAF_ChangeDetection_ANN/tree/master/tools](https://github.com/Albertobegue/PAF_ChangeDetection_ANN/tree/master/tools) contains a few python functions we use in our code (as methods of
evaluation of the result for example)

In the root directory, there are the main functions
(the construction of the Neural Network model with tensorflow, the statistical
methods…) and the other directories contain either data or a few useful
functions to pre-process our data or help us in the main code.

There are also evaluation functions which we use to see
if the predictions by the models are good or not.

**Some more details about neural networks**
As one may know, all neural networks are trained on a labelled dataset. It means that they learn from this dataset (by recalculating the weights and biases that connect them in the purpose of reducing the cost function (a function that evaluates the error between the guess of the network and the label)). 
In their simplest form, there are inputs, then hidden layers and then the output. But in order to manage sequential data, neural networks need to remember their previous outputs. To do that Recurrent Neural Networks loop their outputs to their inputs, which is very useful to take the previous outputs into account in the gradient descent but which implies a vanishing gradient issue (the gradient quickly vanishes to zero which does not allow to pursue the calculation). Hopefully, researchers built neural networks that avoid this issue. They are called LSTM (Long Short Term Memory, see the link above) and are made of special cells (constituted by different layers) that make us forget the vanishing gradient problem ! 

To implement these neural networks, we used tensorflow.

**Report**

[Report](https://github.com/Albertobegue/PAF_ChangeDetection_ANN/blob/master/report.adoc)

 
