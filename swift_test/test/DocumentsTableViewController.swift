//
//  DocumentsTableViewController.swift
//  test
//
//  Created by Keshav Maheshwari on 4/2/20.
//  Copyright © 2020 Masayoshi Iwasa. All rights reserved.
//

import Foundation
import UIKit

class DocumentsTableViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UISearchBarDelegate {
    
    @IBOutlet weak var searchBar: UISearchBar!
    let MainVC = MainViewController()
    
    let documents: [String] = ["Criminal Complaint Application(Court)", "Criminal Complaint Application(Justice Dept)", "Police Department Arrest Booking Form", "Arrest Report", "Offense/Incident Report", "Supplemental Report", "Criminal Complaint", "Incident Report", "Court Activity Record Information"]
    
    let cellReuseIdentifier = "cell"
    
    @IBOutlet weak var tableView: UITableView!
    
    var filteredDocuments: [String]!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        self.tableView.register(UITableViewCell.self, forCellReuseIdentifier: cellReuseIdentifier)
        self.tableView.tableFooterView = UIView()
        
        tableView.delegate = self
        tableView.dataSource = self
        
        tableView.rowHeight = 60
        
        searchBar.delegate = self
        filteredDocuments = documents
    }
    
    override func viewDidAppear(_ animated: Bool) {

        self.tabBarController?.navigationItem.title = "Choose Document Type"
        self.navigationController?.navigationBar.isHidden = true
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return self.filteredDocuments.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell:UITableViewCell = (self.tableView.dequeueReusableCell(withIdentifier: cellReuseIdentifier) as UITableViewCell?)!
        
        cell.textLabel?.text = self.filteredDocuments[indexPath.row]
        
        return cell
    }
    
    func searchBar(_ searchBar: UISearchBar, textDidChange searchText: String) {
        filteredDocuments = searchText.isEmpty ? documents : documents.filter { (item: String) -> Bool in
            // If dataItem matches the searchText, return true to include it
            return item.range(of: searchText, options: .caseInsensitive, range: nil, locale: nil) != nil
        }
        
        tableView.reloadData()
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        print("You tapped cell number \(indexPath.row).")
        MainVC.pickedDocument = documents[indexPath.row]
        print("picked document = \(MainVC.pickedDocument)")
        
        let storyBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)

        let nextViewController = storyBoard.instantiateViewController(withIdentifier: "MainViewController") as! MainViewController
        nextViewController.modalPresentationStyle = .popover
        self.present(nextViewController, animated:true, completion:nil)
    }
    
}
