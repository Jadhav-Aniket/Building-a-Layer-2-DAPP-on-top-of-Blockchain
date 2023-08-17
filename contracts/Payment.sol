// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

// Contract Payment
contract Payment {
    // global variables to store users total and accounts total.
    uint public numUsers = 0;
    uint public AccountTotal = 0;

    //struture to store user
    struct User {
        uint UserId;
        string UserName;
        bool exists;
    }

    //structure to store account exixtance
    struct accounts_exist {
        uint userid1;
        uint userid2;
    }

    //structure to store  joint account
    struct account {
        uint UserId1;
        uint UserId2;
        uint balance;
        bool exists;
    }

    uint[1000] public transactions;
    uint public txcount = 0;

    //Mappings
    mapping(uint => User) public Users;
    mapping(uint => accounts_exist) public accounts;
    mapping(uint => mapping(uint => account)) public jointAccounts;

    //function to register user
    function registerUser(
        uint UserId,
        string memory UserName
    ) public returns (string memory) {
        //if user exist return else registers
        if (Users[UserId].exists) {
            return ("User already exists");
        }

        Users[UserId] = User(UserId, UserName, true);
        numUsers++;
        return ("User Registered");
    }

    //display all joint accounts details
    function getAllAccounts() public view returns (account[] memory) {
        account[] memory result = new account[](2 * AccountTotal);
        uint j = 0;
        // loop over total accounts and displays accounts
        for (uint i = 0; i < AccountTotal; i++) {
            uint userid1 = accounts[i].userid1;
            uint userid2 = accounts[i].userid2;
            result[j++] = jointAccounts[userid1][userid2];
            result[j++] = jointAccounts[userid2][userid1];
        }
        return result;
    }

    // function to create joint accounts for two users
    function createJointAccount(
        uint userId1,
        uint userId2,
        uint256 balance
    ) public returns (string memory) {
        if (userId1 == userId2) {
            return ("Cannot create joint account with same user");
        }

        if (!Users[userId1].exists || !Users[userId2].exists) {
            return ("Users does not already exists");
        }

        jointAccounts[userId1][userId2] = account(
            userId1,
            userId2,
            balance / 2,
            true
        );
        jointAccounts[userId2][userId1] = account(
            userId2,
            userId1,
            balance / 2,
            true
        );
        accounts[AccountTotal++] = accounts_exist(userId1, userId2);
        return ("Account Created");
    }

    //function used to store amount from one sender to other sender.
    function sendAmount(uint amount, uint[] memory path) public returns (uint) {
        //first checks if transaction is possible or not
        for (uint i = 0; i < path.length - 1; i++) {
            uint node1 = path[i];
            uint node2 = path[i + 1];
            if (jointAccounts[node1][node2].balance < amount) {
                transactions[txcount++] = 0;
                return 0;
            }
        }
        // perform transaction
        for (uint i = 0; i < path.length - 1; i++) {
            uint node1 = path[i];
            uint node2 = path[i + 1];
            jointAccounts[node1][node2].balance =
                jointAccounts[node1][node2].balance -
                amount;
            jointAccounts[node2][node1].balance =
                jointAccounts[node2][node1].balance +
                amount;
        }
        transactions[txcount++] = 1;
        return 1;
    }

    // return the saved status of transactions (0-invalid,1-valid)
    function TXstatus() public view returns (uint256[] memory) {
        uint256[] memory Txlist = new uint256[](1000);
        for (uint i = 0; i < transactions.length; i++) {
            Txlist[i] = transactions[i];
        }
        return Txlist;
    }

    //close the joint account created earlier.
    function closeAccount(
        uint userId1,
        uint userId2
    ) public returns (string memory) {
        if (!jointAccounts[userId1][userId2].exists) {
            return ("Joint account does not exist");
        }

        jointAccounts[userId1][userId2] = account(userId1, userId2, 0, false);
        jointAccounts[userId2][userId1] = account(userId2, userId1, 0, false);
        return ("Account Deleted");
    }
}
