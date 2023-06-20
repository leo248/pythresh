# pythresh -> T-Threshold Scheme After David Jungnickel

This is an implementation of a t-threshold scheme as described by David Jungnickel. This scheme is a cryptographic concept that allows a secret to be shared among a group of participants in such a way that only when a certain threshold of participants come together, the secret can be reconstructed.

## Disclaimer

This project is for academic purposes only. The contributors take no responsibility for any misuse or damages resulting from the use of this software. The software is provided as is, without warranty of any kind, express or implied. The users are solely responsible for their use of the software. 

## Prerequisites

Before running the program, you need to have the following libraries installed on your local system:

- argparse
- itertools
- random
- numpy

You also need to have [SageMath](https://www.sagemath.org/download.html) installed. 


## To-Do List

### First:
- [ ] Reconstruct the hyperplane as a P.subscheme instead of a list of points.
- [ ] Investigate different methods for reconstructing the hyperplane. (also as a subscheme)
- [ ] Define lines as P.subschemes instead of lists of points.

### Second:
- [ ] Create standalone functions or minimize dependency on SageMath.

### Third:
- [ ] Consider recreating the implementation in Rust.
- [ ] Improve the run time of the algorithm.

### Fourth:
- [ ] Add a RSA layer to transfer the partial secret

## Contributing

Contributions are very welcome.

## Acknowledgements

This project was inspired by and follows the principles laid out by David Jungnickel in his work on t-threshold schemes. I would like to express our gratitude for his significant contributions to this field.

For more information on this and other cryptographic concepts, please refer to David Jungnickel's research papers and books.


## Usage
![Usage Image](/usage.png)
