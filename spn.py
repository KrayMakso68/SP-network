"""
The `spn` module implements the Substitution-Permutation Network (SPN) encryption algorithm.

SPN is a symmetric-key block cipher that operates on fixed-size blocks of plaintext and produces
corresponding blocks of ciphertext. It consists of several rounds of substitutions and permutations
and key additions applied to the input data.

Classes:
- SPN: Implementation of the SPN encryption algorithm.

Usage:
Initialize an instance of the `SPN` class with the required parameters, then use the provided methods
to perform encryption and decryption operations.
"""
from math import log2

__all__ = ["gen_pbox", "SPN", "int_to_str_with_fill"]


def gen_pbox(s, n):
    """
    Generate a balanced permutation box for an SPN.

    Parameters
    ----------
    s : int
        Number of bits per S-box.
    n : int
        Number of S-boxes.

    Returns
    -------
    list of int
        The generated P-box.

    """
    return [(s * i + j) % (n * s) for j in range(s) for i in range(n)]


def int_to_str_with_fill(num, str_len):
    """
    Convert an integer to a byte string with fill character.

    Parameters
    ----------
    num: int
        Integer to convert.
    str_len: int
        Length of string to convert.

    Returns
    -------
    str
        Byte string.

    """
    fill = str_len
    return "{0:b}".format(num).zfill(fill)


class SPN:
    """
    Class representing the SPN (Substitution-Permutation Network) encryption algorithm.

    Methods
    -------
    perm(inp)
        Apply the P-box permutation on the input.
    inv_perm(inp)
        Apply the inverse P-box permutation on the input.
    sub(inp)
        Apply the S-box substitution on the input.
    inv_sub(inp)
        Apply the inverse S-box substitution on the input.
    _enc_last_noperm(pt)
        Encrypt plaintext using the SPN, where the last round doesn't contain the permute operation.
    _enc_last_withperm(ct)
        Encrypt plaintext using the SPN, where the last round contains the permute operation.
    _dec_last_noperm(ct)
        Decrypt ciphertext using the SPN, where the last round doesn't contain the permute operation.
    _dec_last_withperm(ct)
        Decrypt ciphertext using the SPN, where the last round contains the permute operation.
    """

    def __init__(self, sbox, pbox, key, rounds, implementation=0):
        """
        Initialize the SPN class with the provided parameters.

        Parameters
        ----------
        sbox : list of int
            List of integers representing the S-box.

        pbox : list of int
            List of integers representing the P-box.

        key : int
            Key value

        rounds : int
            Number of rounds for the SPN. (full rounds)

        implementation : int, optional
            Implementation option. Default is 0.
            0: Last round doesn't contain the permute operation.
            1: Last round contains the permute operation.
        """
        self.sbox = sbox
        self.pbox = pbox
        self.sinv = [sbox.index(i) for i in range(len(sbox))]
        self.pinv = [pbox.index(i) for i in range(len(pbox))]
        self.block_size = len(pbox)
        self.box_size = int(log2(len(sbox)))
        self.num_sbox = len(pbox) // self.box_size
        self.rounds = rounds
        self.key = key
        if implementation == 0:
            self.encrypt = self._enc_last_noperm
            self.decrypt = self._dec_last_noperm
        else:
            self.encrypt = self._enc_last_withperm
            self.decrypt = self._dec_last_withperm

    def perm(self, inp: int) -> int:
        """
        Apply the P-box permutation on the input.

        Parameters
        ----------
        inp : int
            The input value to apply the P-box permutation on.

        Returns
        -------
        int
            The permuted value after applying the P-box.
        """
        ct = 0
        for i, v in enumerate(self.pbox):
            ct |= (inp >> (self.block_size - 1 - i) & 1) << (
                    self.block_size - 1 - v)
        return ct

    def inv_perm(self, inp: int) -> int:
        """
        Apply the inverse P-box permutation on the input.

        Parameters
        ----------
        inp : int
            The input value to apply the inverse P-box permutation on.

        Returns
        -------
        int
            The permuted value after applying the inverse P-box.
        """
        ct = 0
        for i, v in enumerate(self.pinv):
            ct |= (inp >> (self.block_size - 1 - i) & 1) << (
                    self.block_size - 1 - v)
        return ct

    def sub(self, inp: int) -> int:
        """
        Apply the S-box substitution on the input.

        Parameters
        ----------
        inp : int
            The input value to apply the S-box substitution on.

        Returns
        -------
        int
            The substituted value after applying the S-box.
        """
        ct, bs = 0, self.box_size
        for i in range(self.num_sbox):
            ct |= self.sbox[(inp >> (i * bs)) & ((1 << bs) - 1)] << (bs * i)
        return ct

    def inv_sub(self, inp: int) -> int:
        """
        Apply the inverse S-box substitution on the input.

        Parameters
        ----------
        inp : int
            The input value to apply the inverse S-box substitution on.

        Returns
        -------
        int
            The substituted value after applying the inverse S-box.
        """
        ct, bs = 0, self.box_size
        for i in range(self.num_sbox):
            ct |= self.sinv[(inp >> (i * bs)) & ((1 << bs) - 1)] << (bs * i)
        return ct

    def _enc_last_noperm(self, pt: int) -> int:
        """
        Encrypt plaintext using the SPN, where the last round doesn't contain the permute operation.

        Parameters
        ----------
        pt : int
            The plaintext input to be encrypted.

        Returns
        -------
        int
            The ciphertext after encryption.
        """
        ct = pt ^ self.key
        for _ in range(self.rounds):
            ct = self.sub(ct)
            ct = self.perm(ct)
            ct ^= self.key
        ct = self.sub(ct)
        return ct ^ self.key

    def _enc_last_withperm(self, ct: int) -> int:
        """
        Encrypt plaintext using the SPN, where the last round contains the permute operation.
        Note, the last permutation provides no additional security.

        Parameters
        ----------
        ct : int
            The plaintext input to be encrypted.

        Returns
        -------
        int
            The ciphertext after encryption.
        """
        for _ in range(self.rounds):
            ct ^= self.key
            ct = self.sub(ct)
            ct = self.perm(ct)
        return ct ^ self.key

    def _dec_last_noperm(self, ct: int) -> int:
        """
        Decrypt ciphertext using the SPN, where the last round doesn't contain the permute operation.

        Parameters
        ----------
        ct : int
            The ciphertext input to be decrypted.

        Returns
        -------
        int
            The plaintext after decryption.
        """
        ct = ct ^ self.key
        ct = self.inv_sub(ct)
        for _ in range(self.rounds):
            ct ^= self.key
            ct = self.inv_perm(ct)
            ct = self.inv_sub(ct)
        return ct ^ self.key

    def _dec_last_withperm(self, ct: int) -> int:
        """
        Decrypt ciphertext using the SPN, where the last round contains the permute operation.

        Parameters
        ----------
        ct : int
            The ciphertext input to be decrypted.

        Returns
        -------
        int
            The plaintext after decryption.
        """
        ct = ct ^ self.key

        for _ in range(self.rounds):
            ct = self.inv_perm(ct)
            ct = self.inv_sub(ct)
            ct ^= self.key
        return ct
