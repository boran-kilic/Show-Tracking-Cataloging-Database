import sqlite3
import PySimpleGUI as sg
from datetime import date

today = date.today()

con = sqlite3.connect('Project.db')
cur = con.cursor()

layout_login = [[sg.Text('Email:',size=(10,1)), sg.Input(size=(20,1), key='email')],
                [sg.Text('Password',size=(10,1)), sg.Input(size=(20,1), key='password', password_char='*')],
                [sg.Button('Login')],
                [sg.Button('Sign up')]]
          
window = sg.Window('Login Window', layout_login)

login_id = -1

while True:
    event, values = window.read()
    if event == 'Login':
        email = values['email']
        emailtup = (email,)
        password = values['password']
        cur.execute('SELECT * FROM Admin')
        adminlist = cur.fetchall()

        if email == '':
            sg.popup('Missing email!')
        elif password == '':
            sg.popup('Missing password!')
        
        elif emailtup not in adminlist: #USER
          
            cur.execute('SELECT Email FROM Account WHERE Email = ? AND Password = ?', (email,password))
            row = cur.fetchone()
            
            if row is None:
                sg.popup('No such account!')
        
            else:        
                cur.execute('SELECT Name FROM Account WHERE Email = ? AND Password = ?', (email,password))
                name = cur.fetchone()
                login_id = row[0]
                window.close()
                layout_user = [[sg.Text('Welcome, ' + name[0],size=(50,1))],
                       [sg.Button('List all shows')],
                       [sg.Button('My List')],
                        [sg.Button('See All Discussions')],
                       [sg.Button('Logout')]]  
                window = sg.Window('User window', layout_user)
                while True:
                    event, values = window.read()
                    
                    if event == 'See All Discussions':
                        window.close()
                        cur.execute('SELECT S.Name, ID.Description, ID.Disc_Init_Date, ID.Discussion_ID, U.Username FROM Show S, Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Initiated_Show_ID = S.Show_ID')
                        discussions = cur.fetchall()
                        cur.execute('SELECT DISTINCT S.Name FROM Show S, Initiated_Discussion ID WHERE ID.Initiated_Show_ID = S.Show_ID')
                        allshows = cur.fetchall()
                        
                        layout = [[sg.Listbox(discussions, size=(80, len(discussions)), key='chosen_disc')],
                                  [sg.Text('Show:', size=(15,1)), sg.Combo(allshows, size=(15, 4), key='chosen_show')],
                                  [sg.Button('Filter')],
                                  [sg.Button('See Discussion')],
                                  [sg.Button('Create Discussion')],
                                  [sg.Button('Back to Homepage')]]
                        
                        window = sg.Window('Discussions', layout)
                        while True:
                                event, values = window.read() 
                                if event == 'Filter':
                                      window.close()
                                      c_show = values['chosen_show']
                                      filtered = []
                                      for i in discussions:
                                          if i[0] == c_show[0]:
                                             filtered.append(i) 
                                      layout_shows = [[sg.Text('Filtered discussions:')],
                                            [sg.Listbox(filtered, size=(50, len(filtered)), key='chosen_disc')],
                                            [sg.Button('See Discussion')],
                                            [sg.Button('Back to Homepage')]]
                                      window = sg.Window('My shows', layout_shows)
                                      while True:
                                          event, values = window.read()
                                          if event == 'See Discussion':
                                                window.close()
                                                cdisc = values['chosen_disc'][0][3]
                                                cur.execute('SELECT ID.Description, ID.Disc_Init_Date, U.Username FROM Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Discussion_ID = ? ',(cdisc,))
                                                title = cur.fetchone()
                                                
                                                cur.execute('SELECT OP.Opinion_ID, U.Username, OP.Opinion_Text, OP.Opinion_Date FROM User U, OPParticipate OP WHERE OP.Participating_User_Email = U.User_Email AND OP.Discussion_ID = ? ',(cdisc,))
                                                opinions = cur.fetchall()
                                                
                                                layout = [[sg.Text(str(title[2]),size=(15,1))],
                                                                  [sg.Text(str(title[0]),size=(30,1))],
                                                                  [sg.Text(str(title[1]),size=(15,1))],
                                                              
                                                            [sg.Listbox(opinions, size=(100, len(opinions)))],
                                                         
                                                          [sg.Button('Add Opinion')],
                                                          [sg.Button('Back to Homepage')]]
                                                
                                                window = sg.Window('Opinions', layout)
                                                while True:
                                                        event, values = window.read() 
                                                        if event == 'Add Opinion':
                                                            window.close()
                                                            layout = [[sg.Text('Share your opinion!')],
                                                                      [sg.Text('Opinion:', size=(15,1)), sg.Input(key='new_op', size=(30,6))],
                                                                      [sg.Button('Submit')],
                                                                      [sg.Button('Back to Homepage')]] 
                                                            window = sg.Window('Add Opinion', layout)
                                                            while True:
                                                              event, values = window.read() 
                                                              if event == 'Submit':
                                                                  op_text = values['new_op']
                                                                  cur.execute('SELECT MAX(Opinion_ID) FROM OPParticipate')
                                                                  op_id = cur.fetchone()[0] + 1
                       
                                                                  cur.execute('INSERT INTO OPParticipate VALUES(?,?,?,?,?)', (cdisc, op_id, email, op_text, today))
                                                                
                                                                  con.commit()
                                                              
                                   
                                                                  #window.close()
                                                                  sg.popup('You have shared your opinion!')
                                                                  
                                                                  break
                                                              if event == 'Back to Homepage':
                                                                  break
                                                        if event == 'Back to Homepage':
                                                            break
                                                        if event == 'Submit':
                                                            break
                                          if event == 'Back to Homepage':
                                              break
                                          if event == 'Submit':
                                              break
                                if event == 'See Discussion':
                                        window.close()
                                        cdisc = values['chosen_disc'][0][3]
                                        cur.execute('SELECT ID.Description, ID.Disc_Init_Date, U.Username FROM Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Discussion_ID = ? ',(cdisc,))
                                        title = cur.fetchone()
                                        
                                        cur.execute('SELECT OP.Opinion_ID, U.Username, OP.Opinion_Text, OP.Opinion_Date FROM User U, OPParticipate OP WHERE OP.Participating_User_Email = U.User_Email AND OP.Discussion_ID = ? ',(cdisc,))
                                        opinions = cur.fetchall()
                                        
                                        layout = [[sg.Text(str(title[2]),size=(15,1))],
                                                          [sg.Text(str(title[0]),size=(30,1))],
                                                          [sg.Text(str(title[1]),size=(15,1))],
                                                      
                                                    [sg.Listbox(opinions, size=(100, len(opinions)))],
                                                 
                                                  [sg.Button('Add Opinion')],
                                                  [sg.Button('Back to Homepage')]]
                                        
                                        window = sg.Window('Opinions', layout)
                                        while True:
                                                event, values = window.read() 
                                                if event == 'Add Opinion':
                                                    window.close()
                                                    layout = [[sg.Text('Share your opinion!')],
                                                              [sg.Text('Opinion:', size=(15,1)), sg.Input(key='new_op', size=(30,6))],
                                                              [sg.Button('Submit')],
                                                              [sg.Button('Back to Homepage')]] 
                                                    window = sg.Window('Add Opinion', layout)
                                                    while True:
                                                      event, values = window.read() 
                                                      if event == 'Back to Homepage':
                                                          break
                                                      if event == 'Submit':
                                                          op_text = values['new_op']
                                                          cur.execute('SELECT MAX(Opinion_ID) FROM OPParticipate')
                                                          op_id = cur.fetchone()[0] + 1
                                                          cur.execute('INSERT INTO OPParticipate VALUES(?,?,?,?,?)', (cdisc, op_id, email, op_text, today))
                                                          con.commit()
                                                          window.close()
                                                          sg.popup('You have shared your opinion!')
                                                          
                                                          break          
                                                if event == 'Back to Homepage':
                                                    break
                                                if event == 'Submit':
                                                    break
                                if event == 'Create Discussion':
                        
                                      window.close()
                                      cur.execute('SELECT S.Show_ID, S.Name FROM Show S')
                                      allshows = cur.fetchall()
                                      
                                      layout = [[sg.Text('Start by sharing your idea or questions!')],
                                                [sg.Text('Show:', size=(15,1)), sg.Combo(allshows, size=(15, 4), key='chosen_show')],
                                                [sg.Text('Description:', size=(15,1)), sg.Input(key='new_disc', size=(30,6))],
                                                [sg.Button('Submit')],
                                                [sg.Button('Back to Homepage')]] 
                                      window = sg.Window('Add Discussion', layout)
                                      while True:
                                        event, values = window.read() 
                                        if event == 'Submit':
                                            
                                            
                                            sid = values['chosen_show'][0]
                                            
                                            
                                            desc = values['new_disc']
                                            cur.execute('SELECT MAX(Discussion_ID) FROM Initiated_Discussion')
                                            disc_id = cur.fetchone()[0] + 1
                                            cur.execute('INSERT INTO Initiated_Discussion VALUES(?,?,?,?,?)', (desc, today, disc_id, email, sid))
                                            con.commit()
                                            window.close()
                                            sg.popup('You have initiated a discussion!')
                                            
                                            break
                                
                                if event == 'Submit':
                                    window.close()
                                    cur.execute('SELECT S.Name, ID.Description, ID.Disc_Init_Date, ID.Discussion_ID, U.Username FROM Show S, Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Initiated_Show_ID = S.Show_ID')
                                    discussions = cur.fetchall()
                                    cur.execute('SELECT DISTINCT S.Name FROM Show S, Initiated_Discussion ID WHERE ID.Initiated_Show_ID = S.Show_ID')
                                    allshows = cur.fetchall()
                                    
                                    layout = [[sg.Listbox(discussions, size=(80, len(discussions)), key='chosen_disc')],
                                              [sg.Text('Show:', size=(15,1)), sg.Combo(allshows, size=(15, 4), key='chosen_show')],
                                              [sg.Button('Filter')],
                                              [sg.Button('See Discussion')],
                                              [sg.Button('Create Discussion')],
                                              [sg.Button('Back to Homepage')]]
                                    window = sg.Window('Discussions', layout)                                        
                                
                               
                                if event == 'Back to Homepage':
                                    break
                                if event == sg.WIN_CLOSED:
                                    break
                    if(event == 'My List'):
                            window.close()
                            cur.execute('SELECT s.Name, co.Status FROM Show s, contains co, CreatedList C WHERE C.Creator_Email = ? AND co.Containing_List_ID = C.List_ID AND co.Contained_Show_ID = s.Show_ID ', (email,))
                                        
                            showsinlist = cur.fetchall()
                           
                            status_options = ['Completed', 'Watching', 'Dropped','Plan to watch']
                            layout_shows = [[sg.Text('My shows:')],
                                        [sg.Listbox(showsinlist, size=(50, len(showsinlist)))],
                                        [sg.Text('Status:', size=(15,1)), sg.Combo(status_options, size=(15, 4), key='status')],
                                        [sg.Button('Filter')],
                                        [sg.Button('Back to Homepage')]]
    
                            window = sg.Window('My shows', layout_shows)
                            while True:
                                event, values = window.read()                  
                                if event == 'Filter':
                                    
                                  window.close()
                                  status = values['status']
                                  filtered = []
                                  for i in showsinlist:
                                      if i[1] == status:
                                         filtered.append(i) 
                                  layout_shows = [[sg.Text('My shows:')],
                                        [sg.Listbox(filtered, size=(50, len(filtered)))],
                                        [sg.Button('Return to my list')],
                                        [sg.Button('Back to Homepage')]]
                                  window = sg.Window('My shows', layout_shows)
                                  while True:
                                      event, values = window.read()
                                      if event == 'Back to Homepage':
                                            break
                                      if event == sg.WIN_CLOSED:
                                            break 
                                      if event == 'Return to my list':
                                          break 
                                if event == 'Return to my list':
                                    window.close()
                                    cur.execute('SELECT s.Name, co.Status FROM Show s, contains co, CreatedList C WHERE C.Creator_Email = ? AND co.Containing_List_ID = C.List_ID AND co.Contained_Show_ID = s.Show_ID ', (email,))
                                        
                                    showsinlist = cur.fetchall()
                           
                                    status_options = ['Completed', 'Watching', 'Dropped','Plan to watch']
                                    layout_shows = [[sg.Text('My shows:')],
                                        [sg.Listbox(showsinlist, size=(50, len(showsinlist)))],
                                        [sg.Text('Status:', size=(15,1)), sg.Combo(status_options, size=(15, 4), key='status')],
                                        [sg.Button('Filter')],
                                        [sg.Button('Back to Homepage')]]
                                    window = sg.Window('My shows', layout_shows)     
                                if event == 'Back to Homepage': 
                                  break
                                if event == sg.WIN_CLOSED:
                                    break       
                    if(event == 'List all shows'):
                            window.close()
                            cur.execute('SELECT Name FROM Show')
                            choices = cur.fetchall()
                            
                            layout_shows = [[sg.Text('All shows:')],
                                        [sg.Listbox(choices, size=(15, len(choices)), key='chosen_name')],
                                        [sg.Button('See show info')],
                                        [sg.Button('Back to Homepage')]]                                       
                            window = sg.Window('All shows', layout_shows)
                            while True:
                                event, values = window.read()
                                if event == 'See show info':
                                    
                                    
                                    
                                    if values['chosen_name']: # if some row is selected
                                       window.close()
                                       cshow = values['chosen_name'][0][0]
                                       chosenshow = []
                                       cur.execute('SELECT Name, Plot_Summary, Type, Show_ID, Stars, Year, Genre  FROM Show WHERE Name = ?',(cshow,))
                                       row = cur.fetchone()
                                       cshowid= row[3]
                                       chosenshow.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                                       cur.execute('SELECT Score FROM Rating WHERE Rated_Show_ID = ?',(str(chosenshow[0][3]),))
                                       allscores = cur.fetchall()
                                       if len(allscores) != 0:
                                           totalscore = 0
                                           n =0
                                           for s in allscores:
                                               totalscore += int(s[0])
                                               n+=1
                                           averagerating = totalscore/n
                                           f_averagerating = format(averagerating, '.2f')
                                           averageratings = 'score: ' + str(f_averagerating)
                                       else:
                                           averageratings = 'Nobody rated this show'
                                       
                                       layout_show = [[sg.Text(str(chosenshow[0][0]),size=(30,2))],
                                                      [sg.Text(averageratings,size=(30,2))],
                                                      [sg.Text(str(chosenshow[0][1]),size=(30,8))],
                                                      [sg.Text(str(chosenshow[0][2]),size=(10,1))],
                                                      [sg.Text(str(chosenshow[0][4]),size=(30,2))],
                                                      [sg.Text(str(chosenshow[0][5]),size=(10,1))],
                                                      [sg.Text(str(chosenshow[0][6]),size=(10,1))],
                                                      [sg.Button('Add to list')],
                                                       [sg.Button('Rate show')],
                                                       [sg.Button('See Comments')],
                                                       [sg.Button('Back to Homepage')]]
                                       window = sg.Window(str(chosenshow[0][0]), layout_show) 
                                       while True:
                                             event, values = window.read()

                                                             
                                             if event == 'Add to list':
                                                 window.close()
                                                 status_options = ['Completed', 'Watching', 'Dropped','Plan to watch']
                             
                                                # for different elements, we can define size for better looks and alignment
                                                 layout = [[sg.Text('Status:', size=(15,1)), sg.Combo(status_options, size=(15, 4), key='status')],
                                                       
                                                          [sg.Button('Add')],
                                                          [sg.Button('Back to Homepage')]] 
                                                 window = sg.Window('Add to list', layout)
                                                 while True:
                                                     event, values = window.read() 
                                                     
                                                     if event == 'Add':
                                                        
                                                         cur.execute('SELECT DISTINCT co.Contained_Show_ID, co.Containing_List_ID FROM Contains co, CreatedList C WHERE C.Creator_Email = ? AND co.Containing_List_ID = C.List_ID ', (email,))
                                        
                                                         showsinlist = cur.fetchall()
                                                         
                                                         showids = []
                                                         
                                                         for i in showsinlist:
                                                             showids.append(i[0])
                                                         
                                                         if chosenshow[0][3] in showids:
                                                             window.close()
                                                             status = values['status']
                                                             sid = str(chosenshow[0][3])
                                                             cur.execute('SELECT List_ID FROM CreatedList WHERE Creator_Email = ?', (email,))
                                                             lid = cur.fetchone()
                                                             cur.execute('UPDATE Contains SET Status = ? WHERE Contained_Show_ID = ? AND Containing_List_ID = ?', (status,sid,lid[0]))
                                                            
                                                             con.commit()
                                                             sg.popup('Status updated!')
                                                             break
                                                         
                                                         else:
                                                             window.close()
                                                             status = values['status']
                                                             sid = str(chosenshow[0][3])
                                                             cur.execute('SELECT List_ID FROM CreatedList WHERE Creator_Email = ?', (email,))
                                                             lid = cur.fetchone()
                                                             cur.execute('INSERT INTO Contains VALUES(?,?,?)', (status, sid, lid[0]))
                                                             
                                                             con.commit()
                                                             sg.popup('Show added to your list!')
                                                             break
                                                     if event == sg.WIN_CLOSED:
                                                         break
                                             if event == 'Rate show': 
                                                 
                                                 sid = str(chosenshow[0][3])
                                                 cur.execute('SELECT * FROM Rating WHERE Rating_User_Email = ? AND Rated_Show_ID = ?', (email,sid))
                                                 row = cur.fetchone()
                                                 cur.execute('SELECT co.Status FROM Contains co, CreatedList c WHERE co.Containing_List_ID = c.List_ID AND co.Contained_Show_ID = ? AND c.Creator_Email = ?', (sid,email))
                                                 status1 = cur.fetchone()
                                                 L1 = ['Completed', 'Dropped']   
                                                 if row is not None:
                                                     sg.popup('You already rated!')
                                                 elif status1 is None:
                                                     sg.popup('You can only rate the shows in your list!')
                                                     
                                                 elif status1[0] not in L1:
                                                     sg.popup('You can only rate the completed or dropped shows!')
                                                 else:
                                                     window.close()
                                                     layout = [[sg.Text('Rate the show 1-10')],
                                                                 [sg.Text('Rating:', size=(15,1)), sg.Input(key='rating', size=(15,1))],
                                                           
                                                                  [sg.Button('Rate')],
                                                                  [sg.Button('Back to Homepage')]] 
                                                     window = sg.Window('Rate show', layout)
                                                     while True:
                                                         event, values = window.read() 
                                                         if event == 'Rate':
                                                             score = values['rating']
                                                             cur.execute('SELECT MAX(Rate_ID) FROM Rating')
                                                             rate_id = cur.fetchone()[0] + 1
            
                                                             cur.execute('INSERT INTO Rating VALUES(?,?,?,?,?)', (score, today ,rate_id,email,sid))
                                                             
                                                             con.commit()
                                                           
                                                             window.close()
                                                             sg.popup('You have successfully rated this show')
                                                             break
                                                         if event == 'Back to Homepage':
                                                             break
                            
                                                         if event == sg.WIN_CLOSED:
                                                             break
                                                 if event == 'Rate' or event == 'Add':
                                                     break
                                             
                                             if event == 'See Comments':
                                                 
                                                 window.close()
                                                 cur.execute('SELECT U.username, L.Comment_Text, L.Comment_Date FROM LeaveComment L, User U WHERE L.Commenting_User_Email = U.User_Email AND L.Commented_Show_ID = ?',(cshowid,))
                                                 comments = cur.fetchall()
                                                
                                                 layout_comments = [[sg.Text('Comments:')],
                                                            [sg.Listbox(comments, size=(80, len(comments)), key='chosen_name')],
                                                            [sg.Button('Add Comment')],
                                                            [sg.Button('Back to Homepage')]]
                                                            
                                                
                                                 window = sg.Window('Comments', layout_comments)
                                                 while True:
                                                         event, values = window.read() 
                                                         if event == 'Add Comment':
                                                 
                                                              sid = str(chosenshow[0][3])
                                                            
                                                              cur.execute('SELECT co.Status FROM Contains co, CreatedList c WHERE co.Containing_List_ID = c.List_ID AND co.Contained_Show_ID = ? AND c.Creator_Email = ?', (sid,email))
                                                              status1 = cur.fetchone()
                                                              L1 = ['Completed', 'Dropped']   
                                                              
                                                              if status1 is None:
                                                                  sg.popup('You can only comment on the shows in your list!')
                                                              elif status1[0] not in L1:
                                                                  sg.popup('You can only comment on completed or dropped shows!')
                                                              else:
                                                                  window.close()
                                                                  layout = [[sg.Text('Comment on the show')],
                                                                              [sg.Text('Comment:', size=(15,1)), sg.Input(key='comment', size=(30,6))],
                                                                       
                                                                               [sg.Button('Submit')],
                                                                               [sg.Button('Back to Homepage')]] 
                                                                  window = sg.Window('Add comment', layout)
                                                                  while True:
                                                                      event, values = window.read() 
                                                                      if event == 'Submit':
                                                                          
                                                                          ctext = values['comment']
                                                                          cur.execute('SELECT MAX(Comment_ID) FROM LeaveComment')
                                                                          com_id = cur.fetchone()[0] + 1
                        
                                                                          cur.execute('INSERT INTO LeaveComment VALUES(?,?,?,?,?)', (ctext, today, com_id, email, sid))
                                                                         
                                                                          con.commit()
                                                                       
                                            
                                                                          window.close()
                                                                          sg.popup('Your comment is submitted!')
                                                                
                                                                          break
                             
                                                                      if event == 'Back to Homepage':
                                                                          break
                                        
                                                                      if event == sg.WIN_CLOSED:
                                                                          break
                                                         if event == 'Submit':
                                                             window.close()
                                                             cur.execute('SELECT U.username, L.Comment_Text, L.Comment_Date FROM LeaveComment L, User U WHERE L.Commenting_User_Email = U.User_Email AND L.Commented_Show_ID = ?',(cshowid,))
                                                             comments = cur.fetchall()
                                                            
                                                             layout_comments = [[sg.Text('Comments:')],
                                                                        [sg.Listbox(comments, size=(80, len(comments)), key='chosen_name')],
                                                                        [sg.Button('Add Comment')],
                                                                        [sg.Button('Back to Homepage')]]
                                                                        
                                                            
                                                             window = sg.Window('Comments', layout_comments)
                                                         if event == 'Back to Homepage':
                                                             break
                                                         
                                                         if event == sg.WIN_CLOSED:
                                                             break
                                                
                                             
                                             
                                             if event == 'Rate' or event == 'Add':
                                                 break
                                             if event == 'Back to Homepage':
                                                 break

                                             if event == sg.WIN_CLOSED:
                                                 break
                                           
                                        
                                    else: 
                                        sg.popup('You did not choose anything!') 
                                
                                if event == 'Back to Homepage':
                                    break
                                if event == 'Rate' or event == 'Add':
                                    break
                                if event == 'Logout':
                                    break
                                if event == sg.WIN_CLOSED:
                                    break
                    if event == 'Back to Homepage':
                        window.close()
                        layout_user = [[sg.Text('Welcome, ' + name[0],size=(50,1))],
                               [sg.Button('List all shows')],
                               [sg.Button('My List')],
                                [sg.Button('See All Discussions')],
                               [sg.Button('Logout')]]  
                        window = sg.Window('User window', layout_user)      
                    if event == 'Rate' or event == 'Add':
                        window.close()
                        layout_user = [[sg.Text('Welcome, ' + name[0],size=(50,1))],
                               [sg.Button('List all shows')],
                               [sg.Button('My List')],
                                [sg.Button('See All Discussions')],
                               [sg.Button('Logout')]]  
                        window = sg.Window('User window', layout_user)
                    if event == 'Logout':
                                break
                    if event == sg.WIN_CLOSED:
                                    break          
                    
        else: #ADMIN           
           
            cur.execute('SELECT Email FROM Account WHERE Email = ? AND Password = ?', (email,password))
            row = cur.fetchone()
            
            if row is None:
                sg.popup('No such account!')
            else:
                
                cur.execute('SELECT Name FROM Account WHERE Email = ? AND Password = ?', (email,password))
                name = cur.fetchone()
                login_id = row[0]
                window.close()
                layout_admin = [[sg.Text('Welcome, ' + name[0],size=(50,1))],
                       [sg.Button('Add show')],
                       [sg.Button('List all shows')],
                       [sg.Button('See All Discussions')],
                       [sg.Button('Logout')]]  
                window = sg.Window('Admin window', layout_admin)
                
                while True:
                    event, values = window.read()
                    
                    if event == 'See All Discussions':
                        window.close()
                        cur.execute('SELECT S.Name, ID.Description, ID.Disc_Init_Date, ID.Discussion_ID, U.Username FROM Show S, Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Initiated_Show_ID = S.Show_ID')
                        discussions = cur.fetchall()
                        cur.execute('SELECT DISTINCT S.Name FROM Show S, Initiated_Discussion ID WHERE ID.Initiated_Show_ID = S.Show_ID')
                        allshows = cur.fetchall()
                        
                        layout = [[sg.Listbox(discussions, size=(80, len(discussions)), key='chosen_disc')],
                                  [sg.Text('Show:', size=(15,1)), sg.Combo(allshows, size=(15, 4), key='chosen_show')],
                                  [sg.Button('Filter')],
                                  [sg.Button('See Discussion')],
                                  [sg.Button('Delete Discussion')],
                                  [sg.Button('Back to Homepage')]]
                        
                        window = sg.Window('Discussions', layout)
                        while True:
                                event, values = window.read() 
                                if event == 'Back to Homepage': 
                                  break
                                if event == 'Filter':
                                      window.close()
                                      c_show = values['chosen_show']
                                      filtered = []
                                      for i in discussions:
                                          if i[0] == c_show[0]:
                                             filtered.append(i) 
                                      layout_shows = [[sg.Text('Filtered discussions:')],
                                            [sg.Listbox(filtered, size=(50, len(filtered)), key='chosen_disc')],
                                            [sg.Button('See Discussion')],
                                            [sg.Button('Delete Discussion')],
                                            [sg.Button('Back to Homepage')]]
                                      window = sg.Window('My shows', layout_shows)
                                      while True:
                                          event, values = window.read()
                                          if event == 'Back to Homepage': 
                                            break
                                          if event == 'Delete Discussion':
                                                discid = values['chosen_disc'][0][3]
                                                window.close()
                                                layout = [[sg.Text('Are you sure?')],
                                                          
                                                          [sg.Button('Delete')],
                                                          [sg.Button('Cancel')]] 
                                                window = sg.Window('Delete Discussion', layout)
                                                while True:
                                                  event, values = window.read() 
                                                  if event == 'Delete':
                                                      cur.execute('DELETE FROM Initiated_Discussion WHERE Discussion_ID = ? ',(discid,))
                                                      cur.execute('DELETE FROM OPParticipate WHERE Discussion_ID = ? ',(discid,))                                          
                                                      con.commit()
                                                      sg.popup('You have deleted the discussion!')
                                                      break  
                                                  if event == 'Cancel':
                                                      break
                                                  if event == sg.WIN_CLOSED:
                                                      break
                                            
                                          if event == 'See Discussion':
                                                window.close()
                                                cdisc = values['chosen_disc'][0][3]
                                                cur.execute('SELECT ID.Description, ID.Disc_Init_Date, U.Username FROM Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Discussion_ID = ? ',(cdisc,))
                                                title = cur.fetchone()
                                                
                                                cur.execute('SELECT OP.Opinion_ID, U.Username, OP.Opinion_Text, OP.Opinion_Date FROM User U, OPParticipate OP WHERE OP.Participating_User_Email = U.User_Email AND OP.Discussion_ID = ? ',(cdisc,))
                                                opinions = cur.fetchall()
                                                
                                                layout = [[sg.Text(str(title[2]),size=(15,1))],
                                                                  [sg.Text(str(title[0]),size=(30,1))],
                                                                  [sg.Text(str(title[1]),size=(15,1))],
                                                              
                                                            [sg.Listbox(opinions, size=(100, len(opinions)), key='chosen_op')],
                                                         
                                                          [sg.Button('Delete Opinion')],
                                                          [sg.Button('Back to Homepage')]]
                                                
                                                window = sg.Window('Opinions', layout)
                                                while True:
                                                        event, values = window.read() 
                                                        if event == 'Back to Homepage': 
                                                          break
                                                        if event == 'Delete Opinion':
                                                            opid = values['chosen_op'][0][0]
                                                            window.close()
                                                            layout = [[sg.Text('Are you sure?')],
                                                                      
                                                                      [sg.Button('Delete')],
                                                                      [sg.Button('Cancel')]] 
                                                            window = sg.Window('Delete Opinion', layout)
                                                            while True:
                                                              event, values = window.read() 
                                                              if event == 'Cancel':
                                                                  break
                                                              if event == 'Delete':
                                                                 
                                                                  
                                                            
                                                                 
                                                                  cur.execute('DELETE FROM OPParticipate WHERE Opinion_ID = ? ',(opid,))
                                                                
                                                                  con.commit()
                                                                  sg.popup('You have deleted the opinion!')
                                                                  break
                                                        if event == 'Cancel':
                                                            break
                                                        if event == 'Delete':
                                                            break      
                                if event == 'See Discussion':
                                    window.close()
                                    cdisc = values['chosen_disc'][0][3]
                                    cur.execute('SELECT ID.Description, ID.Disc_Init_Date, U.Username FROM Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Discussion_ID = ? ',(cdisc,))
                                    title = cur.fetchone()
                                    
                                    cur.execute('SELECT OP.Opinion_ID, U.Username, OP.Opinion_Text, OP.Opinion_Date FROM User U, OPParticipate OP WHERE OP.Participating_User_Email = U.User_Email AND OP.Discussion_ID = ? ',(cdisc,))
                                    opinions = cur.fetchall()
                                    
                                    layout = [[sg.Text(str(title[2]),size=(15,1))],
                                                      [sg.Text(str(title[0]),size=(30,1))],
                                                      [sg.Text(str(title[1]),size=(15,1))],
                                                  
                                                [sg.Listbox(opinions, size=(100, len(opinions)), key='chosen_op')],
                                             
                                              [sg.Button('Delete Opinion')],
                                              [sg.Button('Back to Homepage')]]
                                    
                                    window = sg.Window('Opinions', layout)
                                    while True:
                                            event, values = window.read() 
                                            if event == 'Back to Homepage': 
                                              break
                                            if event == 'Delete Opinion':
                                                opid = values['chosen_op'][0][0]
                                                window.close()
                                                layout = [[sg.Text('Are you sure?')],
                                                          
                                                          [sg.Button('Delete')],
                                                          [sg.Button('Cancel')]] 
                                                window = sg.Window('Delete Opinion', layout)
                                                while True:
                                                  event, values = window.read() 
                                                  if event == 'Cancel':
                                                      break
                                                  if event == 'Delete':
                                                     
                                                      
                                                
                                                     
                                                      cur.execute('DELETE FROM OPParticipate WHERE Opinion_ID = ? ',(opid,))
                                                    
                                                      con.commit()
                                                      sg.popup('You have deleted the opinion!')
                                                      break
                                                  if event == sg.WIN_CLOSED:
                                                      break
                                            if event == 'Cancel':
                                                break
                                            if event == 'Delete':
                                                break
                                            if event == sg.WIN_CLOSED:
                                                break
                                if event == 'Delete Discussion':
                        
                              
                                    discid = values['chosen_disc'][0][3]
                                    window.close()
                                    layout = [[sg.Text('Are you sure?')],
                                              
                                              [sg.Button('Delete')],
                                              [sg.Button('Cancel')]] 
                                    window = sg.Window('Delete Discussion', layout)
                                    while True:
                                      event, values = window.read() 
                                      if event == 'Cancel':
                                          break
                                      if event == 'Delete':
                                          cur.execute('DELETE FROM Initiated_Discussion WHERE Discussion_ID = ? ',(discid,))
                                          cur.execute('DELETE FROM OPParticipate WHERE Discussion_ID = ? ',(discid,))                                          
                                          con.commit()
                                          sg.popup('You have deleted the discussion!')
                                          
                                          break
                                if event == 'Delete' or event == 'Cancel':
                                    window.close()
                                    cur.execute('SELECT S.Name, ID.Description, ID.Disc_Init_Date, ID.Discussion_ID, U.Username FROM Show S, Initiated_Discussion ID, User U WHERE ID.Initiating_User_Email = U.User_Email AND ID.Initiated_Show_ID = S.Show_ID')
                                    discussions = cur.fetchall()
                                    cur.execute('SELECT DISTINCT S.Name FROM Show S, Initiated_Discussion ID WHERE ID.Initiated_Show_ID = S.Show_ID')
                                    allshows = cur.fetchall()
                                    
                                    layout = [[sg.Listbox(discussions, size=(80, len(discussions)), key='chosen_disc')],
                                              [sg.Text('Show:', size=(15,1)), sg.Combo(allshows, size=(15, 4), key='chosen_show')],
                                              [sg.Button('Filter')],
                                              [sg.Button('See Discussion')],
                                              [sg.Button('Delete Discussion')],
                                              [sg.Button('Back to Homepage')]]
                                    
                                    window = sg.Window('Discussions', layout)                                        
                                if event == sg.WIN_CLOSED:
                                    break
                    
                    
                                      
                    
                    
                    
                    
                    if(event == 'Add show'):
                        window.close()
                                             
                        status_options = ['Full', 'Half', 'Quarter']
                        
                        # for different elements, we can define size for better looks and alignment
                        layout = [[sg.Text('Name:', size=(15,1)), sg.Input(key='name', size=(15,1))],
                                  [sg.Text('Type:', size=(15,1)), sg.Input(key='type', size=(15,1))],
                                  [sg.Text('Genre:', size=(15,1)), sg.Input(key='genre', size=(15,1))],
                                  [sg.Text('Year:', size=(15,1)), sg.Input(key='year', size=(15,1))],
                                  [sg.Text('Stars:', size=(15,1)), sg.Input(key='stars', size=(15,1))],
                                  [sg.Text('Plot_Summary:', size=(15,1)), sg.Input(key='plot_summary', size=(15,1))],
                                  [sg.Button('Insert')],
                                  [sg.Button('Back to Homepage')]]
                                 
                                   
                        window = sg.Window('Add Show Window', layout)
                        
                        while True:
                            event, values = window.read()
                            if event == sg.WIN_CLOSED:
                                break
                            if event == 'Insert':
                            # lets gather the parameters
                                parameters = (values['type'],values['name'],values['genre'],values['plot_summary'],values['year'],values['stars'])
                                if parameters[0] == '':
                                    sg.popup('Type cannot be empty!')
                                    
                                elif parameters[1] == '':
                                    sg.popup('Name cannot be empty!')
                                    
                                elif parameters[2] == '':
                                     sg.popup('Genre cannot be empty!')
                                    
                                elif parameters[3] == '':
                                    sg.popup('Plot Summary cannot be empty!')
                                   
                                elif parameters[4] == '':
                                    sg.popup('Year cannot be empty!')
                                
                                elif parameters[5] == '':
                                    sg.popup('Stars cannot be empty!')
                                 
                                else:
                                  
                                    cur.execute('SELECT MAX(Show_ID) FROM Show')
                                    show_id = cur.fetchone()[0] + 1
                                
                                    parameters =  parameters + (show_id,)
                           
                                    
                                    # execute insert query
                                    cur.execute('INSERT INTO Show VALUES(?,?,?,?,?,?,?)', parameters)
                                    con.commit()
                                    # show success message
                                    sg.popup('Successfully inserted ' + parameters[1] + ' with id: ' + str(parameters[6]))
                        
                            if event == 'Back to Homepage':
                                break
                            if event == sg.WIN_CLOSED:
                                break
     
                    if(event == 'List all shows'):
                            window.close()
                            cur.execute('SELECT Name FROM Show')
                            choices = cur.fetchall()
                            
                            layout_shows = [[sg.Text('All shows:')],
                                        [sg.Listbox(choices, size=(15, len(choices)), key='chosen_name')],
                                        [sg.Button('See show info')],
                                        [sg.Button('Back to Homepage')]
                                        ]
                            window = sg.Window('All shows', layout_shows)
                            while True:
                                event, values = window.read()                                                               
                                if event == 'See show info':
                                    
                                    if values['chosen_name']: # if some row is selected
                                       window.close()
                                       cshow = values['chosen_name'][0][0]
                                       chosenshow = []
                                       cur.execute('SELECT Name, Plot_Summary, Type, Show_ID, Stars, Year, Genre  FROM Show WHERE Name = ?',(cshow,))
                                       row = cur.fetchone()
                                       cshowid= row[3]
                                       chosenshow.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                                       cur.execute('SELECT Score FROM Rating WHERE Rated_Show_ID = ?',(str(chosenshow[0][3]),))
                                       allscores = cur.fetchall()
                                       if len(allscores) != 0:
                                           totalscore = 0
                                           n =0
                                           for s in allscores:
                                               totalscore += int(s[0])
                                               n+=1
                                           averagerating = totalscore/n
                                           f_averagerating = format(averagerating, '.2f')
                                           averageratings = 'score: ' + str(f_averagerating)
                                       else:
                                           averageratings = 'Nobody rated this show'
                                       
                                       layout_show = [[sg.Text(str(chosenshow[0][0]),size=(30,2))],
                                                      [sg.Text(averageratings,size=(30,2))],
                                                      [sg.Text(str(chosenshow[0][1]),size=(30,8))],
                                                      [sg.Text(str(chosenshow[0][2]),size=(10,1))],
                                                      [sg.Text(str(chosenshow[0][4]),size=(30,2))],
                                                      [sg.Text(str(chosenshow[0][5]),size=(10,1))],
                                                      [sg.Text(str(chosenshow[0][6]),size=(10,1))],
                                                
                                                       [sg.Button('See Comments')],
                                                       [sg.Button('Back to Homepage')]]
                                       window = sg.Window(str(chosenshow[0][0]), layout_show) 
                                       while True:
                                             event, values = window.read() 
                                             
                                             
                                             if event == 'See Comments':
                                                 
                                                 window.close()
                                                 cur.execute('SELECT  L.Comment_ID, U.username, L.Comment_Text, L.Comment_Date FROM LeaveComment L, User U WHERE L.Commenting_User_Email = U.User_Email AND L.Commented_Show_ID = ?',(cshowid,))
                                                 comments = cur.fetchall()
                                                 layout_comments = [[sg.Text('Comments:')],
                                                            [sg.Listbox(comments, size=(80, len(comments)), key='chosen_comment')],
                                                            [sg.Button('Delete Comment')],
                                                            [sg.Button('Back to Homepage')]]
                                                            
                                                
                                                 window = sg.Window('Comments', layout_comments)
                                                 while True:
                                                         event, values = window.read() 
                                                         if event == 'Delete Comment':
                                                             
                                                              if values['chosen_comment']: # if some row is selected
                                                                   window.close()
                                                                   ccomid = values['chosen_comment'][0][0]
                                                                   
                                                                   cur.execute('DELETE FROM LeaveComment WHERE Comment_ID = ?', (ccomid,))
                                                                   con.commit()
                                                                   
                                                                   sg.popup('The comment is deleted!')
                                                                   
                                                         
                                                         if event == 'Delete Comment':
                                                             window.close()
                                                             cur.execute('SELECT  L.Comment_ID, U.username, L.Comment_Text, L.Comment_Date FROM LeaveComment L, User U WHERE L.Commenting_User_Email = U.User_Email AND L.Commented_Show_ID = ?',(cshowid,))
                                                             comments = cur.fetchall()
                                                             layout_comments = [[sg.Text('Comments:')],
                                                                        [sg.Listbox(comments, size=(80, len(comments)), key='chosen_comment')],
                                                                        [sg.Button('Delete Comment')],
                                                                        [sg.Button('Back to Homepage')]]
                                                                        
                                                            
                                                             window = sg.Window('Comments', layout_comments)
                                                         if event == 'Back to Homepage':
                                                             break
                                        
                                                         if event == sg.WIN_CLOSED:
                                                             break                                                                
                                             if event == 'Back to Homepage':
                                                 break
                                        
                                             if event == sg.WIN_CLOSED:
                                                 break        
                                                  
                                if event == 'Back to Homepage':
                                    break
                                        
                                if event == sg.WIN_CLOSED:
                                    break                

                  
                                                           
                    
                    if event == 'Back to Homepage':
                       window.close()
                       layout_admin = [[sg.Text('Welcome, ' + name[0],size=(50,1))],
                              [sg.Button('Add show')],
                              [sg.Button('List all shows')],
                              [sg.Button('See All Discussions')],
                              [sg.Button('Logout')]]  
                       window = sg.Window('Admin window', layout_admin)
                    
                    if event == 'Logout':
                        break
                    if event == sg.WIN_CLOSED:
                        break      
    
    if event == 'Sign up':
            event = ''
            window.close()
            layout_signup = [[sg.Text('Name',size=(10,1)), sg.Input(size=(20,1), key='name')],
                   [sg.Text('Surname',size=(10,1)), sg.Input(size=(20,1), key='surname')],
                   [sg.Text('Email:',size=(10,1)), sg.Input(size=(20,1), key='email')],
                   [sg.Text('Password',size=(10,1)), sg.Input(size=(20,1), key='password')],
                   [sg.Text('Username',size=(10,1)), sg.Input(size=(20,1), key='username')],
                   [sg.Button('Sign up')]]
                   
            window = sg.Window('Sign up Window', layout_signup)
            while True:
                event, values = window.read()
                if event == 'Sign up':
                    name = values['name']
                    surname = values['surname']
                    username = values['username']
                    usertup = (username,)
                    email = values['email']
                    emailtup = (email,)
                    password = values['password']
                    cur.execute('SELECT Username FROM User')
                    username_list = cur.fetchall()
                    cur.execute('SELECT User_Email FROM User')
                    email_list = cur.fetchall()
                    
                    accpara = (values['email'],values['password'],values['name'],values['surname'])
                    
                    if email == '':
                        sg.popup('Missing email!')
                    elif password == '':
                        sg.popup('Missing password!')
                    elif name == '':
                        sg.popup('Missing name!')
                    elif surname == '':
                        sg.popup('Missing surname!')
                    elif username == '':
                        sg.popup('Missing username!')    
                    
                    elif emailtup in email_list:
                        sg.popup('Your E-mail should be unique!')  
                    
                    elif usertup in username_list :
                        sg.popup('Your Username should be unique!')  
                    else:  
                        cur.execute('INSERT INTO Account VALUES(?,?,?,?)', accpara)
                        cur.execute('INSERT INTO User VALUES(?,?)', (username, email))
                        
                        cur.execute('SELECT MAX(List_ID) FROM CreatedList')
                        list_id = cur.fetchone()[0] + 111
                        cur.execute('INSERT INTO CreatedList VALUES(?,?)', (list_id, email))        
                        con.commit()
                      
                        sg.popup('You have signed up succesfully!')
                        event = 'Logout'
                        break
                if event == sg.WIN_CLOSED:
                    break
                           
            

    if event == 'Logout':
        # back to Login Window
        window.close()
        
        layout_login = [[sg.Text('Email:',size=(10,1)), sg.Input(size=(20,1), key='email')],
                        [sg.Text('Password',size=(10,1)), sg.Input(size=(20,1), key='password', password_char='*')],
                        [sg.Button('Login')],
                        [sg.Button('Sign up')]]
                  
        window = sg.Window('Login Window', layout_login)
    
    if event == sg.WIN_CLOSED:
        break
        
window.close()
con.commit()
con.close()