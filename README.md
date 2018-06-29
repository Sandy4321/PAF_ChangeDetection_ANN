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

**Result**

All the results can be found in the folder results.
Our implementation of the method CUSUM is a little bit simple, and we use the library changepoint of R to apply the method of Bayesian.
The scatter plot of the precision and the recall of two methods on different samples:
![Precision and recall](https://github.com/Albertobegue/PAF_ChangeDetection_ANN/blob/master/results/scatterplot_precision_recall.png)
In terms of the neural network, we have implemented two models. These two models have already been trained and are ready to be reused in the files of '.h5' and '.json'. One detects in a small piece of a whole sequence whether there is a change point. In this case, the model would not detect the position of the change point. The other model detect directly the positions of the change points in a sequence. Before giving the data into the model, we have applied a pre-treatment. Every data value will be substracted by the minimum value of the sequence.
The second model is trained by an artificial data set named 'artificial_dataset' in rtt_series and tested also by an artificial data set named 'valid_data'. This model uses a bidirectional LSTM of 32 parameters. It takes every point as an input and determines at the same position whether a changement has happened represented by 0 / 1. It seems that this model works well in many cases. Here is an example:
![Detection of a sample](https://github.com/Albertobegue/PAF_ChangeDetection_ANN/blob/master/results/capture%20l'%C3%A9cran.png)
However, this model works not so well on the real data set named 'real_trace_labelled'. It makes many mistakes in the prediction of the positions.

**Questions**

[Questions about Neural Network](https://github.com/Albertobegue/PAF_ChangeDetection_ANN/blob/master/report.adoc)

 
