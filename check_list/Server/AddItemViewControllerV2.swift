//
//  AddItemViewController.swift
//  CheckListsV3
//
//  Created by Myoung-Wan Koo on 2018. 5. 30..
//  Copyright © 2018년 Myoung-Wan Koo. All rights reserved.
//

import UIKit

class AddItemViewController: UITableViewController{
    @IBAction func cancel(){
        dismiss(animated: true, completion: nil)
        //navigationController?.popViewController(animated: true)
    }
    
    @IBAction func done() {
        dismiss(animated: true, completion: nil)
        //navigationController?.popViewController(animated: true)
    }
    
    override func tableView(_ tableView: UITableView, willSelectRowAt indexPath: IndexPath) -> IndexPath? {
        return nil
    }
}
