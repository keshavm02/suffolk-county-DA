//
//  DocumentsTableViewController.swift
//  test
//
//  Created by Keshav Maheshwari on 4/2/20.
//  Copyright © 2020 Masayoshi Iwasa. All rights reserved.
//

import Foundation
import UIKit

class DocumentsTableViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    let MainVC = MainViewController()
    
    let documents: [String] = ["Criminal Complaint Application(Court)", "Criminal Complaint Application(Justice Dept)", "Police Department Arrest Booking Form", "Arrest Report", "Offense/Incident Report", "Supplemental Report", "Criminal Complaint", "Incident Report", "Court Activity Record Information"]
    
    let cellReuseIdentifier = "cell"
    
    @IBOutlet weak var tableView: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.tableView.register(UITableViewCell.self, forCellReuseIdentifier: cellReuseIdentifier)
        self.tableView.tableFooterView = UIView()
        
        tableView.delegate = self
        tableView.dataSource = self
        
        tableView.rowHeight = 60
        
    }
    
    override func viewDidAppear(_ animated: Bool) {

        self.tabBarController?.navigationItem.title = "Choose Document Type"
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.documents.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell:UITableViewCell = (self.tableView.dequeueReusableCell(withIdentifier: cellReuseIdentifier) as UITableViewCell?)!
        
        cell.textLabel?.text = self.documents[indexPath.row]
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        print("You tapped cell number \(indexPath.row).")
        MainVC.pickedDocument = documents[indexPath.row]
        print("picked document = \(MainVC.pickedDocument)")
    }
    
}
