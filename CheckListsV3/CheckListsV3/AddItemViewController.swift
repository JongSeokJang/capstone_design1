//
//  AddItemViewController.swift
//  CheckListsV3
//
//  Created by Myoung-Wan Koo on 2018. 6. 8..
//  Copyright © 2018년 Myoung-Wan Koo. All rights reserved.
//

import UIKit

class AddItemViewController: UITableViewController,UITextFieldDelegate {

    @IBOutlet weak var doneBarButton: UIBarButtonItem!
    
    @IBOutlet weak var textField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        /* No Large Ttitle */
        navigationItem.largeTitleDisplayMode = .never
    }
    @IBAction func cancel() {
        navigationController?.popViewController(animated: true)
    }
    @IBAction func done() {
        navigationController?.popViewController(animated: true)
        print(" Content of the text field:\(textField.text!)")
    }
    
    override func tableView(_ tableView: UITableView, willSelectRowAt indexPath: IndexPath) -> IndexPath? {
        return nil
    }
    
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        textField.becomeFirstResponder()
        
    }
    
    func textField(_ textField: UITextField,
                   shouldChangeCharactersIn range: NSRange,
                   replacementString string: String) -> Bool {
        
        let oldText = textField.text! as NSString
        let newText = oldText.replacingCharacters(in: range, with: string) as NSString
        print("\(oldText),   \(newText)")
        
        doneBarButton.isEnabled = (newText.length > 0)
        return true
    }

}
